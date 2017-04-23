from tools.workers import Worker
import multiprocessing
import tensorflow as tf

class EvaluationTask(object):
    def __init__(self, data, checkpoint, use_queue=False):
        self.data = data
        self.checkpoint = checkpoint
        self.use_queue = use_queue

    def __call__(self):
        return self.evaluate()

    def evaluate(self):
        with tf.Session() as self.sess:
            self.saver = tf.train.Saver()
            self.saver.restore(self.sess, self.checkpoint)
            self.x = tf.get_collection('x')[0]
            self.y_hat = tf.get_collection('y_hat')[0]
            self.accuracy = tf.get_collection('accuracy')[0]
            if self.use_queue:
                return self.queue_evaluate()
            else:
                return self.feed_dict_evaluate()

    def feed_dict_evaluate(self):
        data_iterator = self.data.get_data_iterator()
        total_accuracy = [] # list that holds the accuracy for each batch
        while True:
            try:
                input_batch, label_batch = next(data_iterator)
                total_accuracy.append(
                    self.sess.run(self.accuracy,
                                  feed_dict={self.x: input_batch,
                                             self.y_hat: label_batch})
                )
            except StopIteration:
                break
        total_accuracy = sum(total_accuracy) / len(total_accuracy)
        print("Accuracy: %g" % total_accuracy)
        return {'accuracy': total_accuracy}

    def queue_evaluate(self):
        raise NotImplementedError()

def launch_evaluation_task(data, checkpoint):
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    worker =  Worker(tasks, results)
    worker.start()
    task = EvaluationTask(data, checkpoint)
    tasks.put(task)
    tasks.put(None)
    result = results.get()
    return result
