from tools.workers import IteratorWorker
import multiprocessing
import tensorflow as tf

class TrainingTask(object):
    def __init__(self, data, checkpoint=None, use_queue=False, iteration_period=1000, save_period=1):
        self.data = data
        self.checkpoint = checkpoint
        self.use_queue = use_queue
        self.iteration_period = iteration_period
        self.save_period = save_period

    def __call__(self):
        return self.train()

    def train(self):
        self.sess = tf.Session()
        self.saver = tf.train.Saver()
        if self.checkpoint is None:
            self.sess.run(tf.global_variables_initializer())
        else:
            self.saver.restore(self.sess, self.checkpoint)
            print("Restored checkpoint \"%s\"" % (self.checkpoint))
        self.writer = tf.summary.FileWriter('logs', self.sess.graph)
        self.x = tf.get_collection('x')[0]
        self.y_hat = tf.get_collection('y_hat')[0]
        self.train_step = tf.get_collection('train_step')[0]
        self.accuracy = tf.get_collection('accuracy')[0]
        self.merged_summaries = tf.get_collection('merged_summaries')[0]
        if self.use_queue:
            return self.queue_train()
        else:
            return self.feed_dict_train()

    def feed_dict_train(self):
        i = 0
        epoch = 0
        data_iterator = self.data.get_data_iterator()
        while True:
            try:
                input_batch, label_batch = next(data_iterator)
            except StopIteration:
                data_iterator = self.data.get_data_iterator()
                input_batch, label_batch = next(data_iterator)
                epoch += 1
                if epoch % self.save_period == 0:
                    print("Starting epoch %d.\nSaving model..." % (epoch))
                    checkpoint_path = self.saver.save(self.sess, 'logs/backup', global_step=epoch)
                    print("Model saved.")
            self.sess.run(self.train_step, feed_dict={self.x: input_batch, self.y_hat: label_batch})
            if i % self.iteration_period == 0:
                train_accuracy = self.sess.run(self.accuracy, feed_dict={self.x: input_batch, self.y_hat: label_batch})
                print("Training accuracy at step %d: %g" % (i, train_accuracy))
                summary = self.sess.run(self.merged_summaries, feed_dict={self.x: input_batch, self.y_hat: label_batch})
                self.writer.add_summary(summary, epoch)
                yield {'train_accuracy': train_accuracy}
            i += 1

    def queue_train(self):
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=self.sess, coord=coord)
        i = 0
        try:
            while not coord.should_stop():
                self.sess.run(self.train_step)
                if i % self.iteration_period == 0:
                    train_accuracy = self.sess.run(self.accuracy)
                    print("Training accuracy at step %d: %g" % (i, train_accuracy))
                    yield {'train_accuracy': train_accuracy}
                i += 1
        except tf.errors.OutOfRangeError:
            print('Training complete. A total of %d iterations were made.' % i)
        finally:
            coord.request_stop()
        coord.join(threads)

def launch_training_task(data, checkpoint=None, use_queue=False, iteration_period=1000, save_period=1):
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    worker = IteratorWorker(tasks, results)
    worker.start()
    task = TrainingTask(data, checkpoint, use_queue, iteration_period, save_period)
    tasks.put(task)
    tasks.put(None)
    while True:
        result = results.get()
        yield result
