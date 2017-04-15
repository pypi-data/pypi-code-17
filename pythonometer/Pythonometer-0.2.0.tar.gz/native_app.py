import Tkinter
from ttk import Style

from pythonometer.quiz import Quiz
from pythonometer.questions.base import WrongAnswer


class TkApp(object):
    def __init__(self, master):
        self.master = master
        self.quiz = Quiz()

        self.question_frame = Tkinter.Frame(self.master, padx=0, pady=0)

        self.question_label = Tkinter.Label(
            self.question_frame, text='Question:', anchor=Tkinter.W, padx=2, pady=2)
        self.question_box = Tkinter.Text(
            self.question_frame, width=5, height=10, relief=Tkinter.FLAT,
            padx=20, pady=20, wrap=Tkinter.WORD, takefocus=0
        )

        self.button_frame = Tkinter.Frame(self.question_frame, padx=0, pady=0)

        self.feedback_label = Tkinter.Label(
            self.question_frame, text='Feedback:', anchor=Tkinter.W, padx=2, pady=2)
        self.feedback_box = Tkinter.Text(
            self.question_frame, width=5, height=2, relief=Tkinter.FLAT,
            padx=20, pady=20, wrap=Tkinter.WORD, takefocus=0
        )

        self.results_label = Tkinter.Label(
            self.question_frame, text='Results:', anchor=Tkinter.W, padx=2, pady=2)
        self.results_box = Tkinter.Text(
            self.question_frame, width=5, height=10, relief=Tkinter.FLAT,
            padx=20, pady=20, wrap=Tkinter.WORD, takefocus=0
        )

        self.submit_button = Tkinter.Button(
            self.button_frame, text='Submit Answer', command=self.handle_response
        )
        self.next_button = Tkinter.Button(
            self.button_frame, text='Skip This Question', command=self.skip_question
        )
        self.answer_box = Tkinter.Text(self.master, height=5, width=20)

        self.layout_widgets()
        self.feedback_box.insert(
            Tkinter.END,
            "Welcome to Pythonometer!\n\nFeedback on your answers will appear here."
        )
        self.show_question()
        self.show_results()

    def layout_widgets(self):
        self.master.wm_attributes('-zoomed', 1)
        self.master.configure(bg='#151517')

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.rowconfigure(0, weight=1)

        self.question_frame.grid(
            row=0,
            column=0,
            sticky=Tkinter.E + Tkinter.W + Tkinter.N + Tkinter.S,
            padx=(40, 10),
        )
        self.question_frame.configure(bg='#252527')
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.question_label.pack(fill=Tkinter.X)
        self.question_label.configure(bg='#303032', fg='#aaa')

        self.question_box.pack(fill=Tkinter.BOTH, expand=1)
        self.question_box.configure(bg='#252527', fg='#ccc', font=('Helvetica', 12), state='disabled', highlightthickness=0)

        self.button_frame.configure(bg='#252527', bd=0)
        self.button_frame.pack(fill=Tkinter.X)

        self.feedback_label.pack(fill=Tkinter.X)
        self.feedback_label.configure(bg='#303032', fg='#aaa')

        self.feedback_box.pack(fill=Tkinter.BOTH, expand=1)
        self.feedback_box.configure(bg='#252527', fg='#ccc', font=('Helvetica', 12), state='disabled', highlightthickness=0)

        self.results_label.pack(fill=Tkinter.X)
        self.results_label.configure(bg='#303032', fg='#aaa')

        self.results_box.pack(fill=Tkinter.BOTH, expand=1)
        self.results_box.configure(bg='#252527', fg='#ccc', font=('Helvetica', 10), state='disabled', highlightthickness=0)

        self.next_button.grid(row=0, column=0, padx=10, pady=10, sticky=Tkinter.E + Tkinter.W)
        self.next_button.configure(bg='#151517', fg='#ccc', relief=Tkinter.FLAT, width=5, highlightthickness=0)
        self.submit_button.grid(row=0, column=1, padx=10, pady=10, sticky=Tkinter.E + Tkinter.W)
        self.submit_button.configure(bg='#151517', fg='#ccc', relief=Tkinter.FLAT, width=5, highlightthickness=0)

        self.answer_box.bind('<<Paste>>', lambda x: 'break')
        self.answer_box.bind('<<PasteSelection>>', lambda x: 'break')
        self.answer_box.configure(
            bg='#151517', fg='#ccc', insertbackground='#ccc', bd=0, font=('Courier', 12), highlightthickness=0)
        self.answer_box.grid(
            row=0,
            column=1,
            padx=20,
            pady=20,
            sticky=Tkinter.E + Tkinter.W + Tkinter.N + Tkinter.S,
        )
        self.answer_box.focus_set()

    def handle_response(self):
        answer = self.answer_box.get('1.0', Tkinter.END)
        try:
            self.quiz.supply_answer(self.quiz.current_question, answer)
            self.answer_box.delete('1.0', Tkinter.END)
            self.show_feedback(True)
            self.show_question()
        except WrongAnswer as e:
            self.show_feedback(False, e)
        self.show_results()

    def skip_question(self):
        try:
            self.quiz.supply_answer(self.quiz.current_question, '')
        except WrongAnswer:
            pass
        self.answer_box.delete('1.0', Tkinter.END)
        self.quiz.next()
        self.show_question()
        self.show_results()

    def show_question(self):
        self.change_text(self.question_box, self.quiz.current_question.get_question_text())

    def show_feedback(self, positive, message=''):
        if positive:
            self.change_text(self.feedback_box, "You're answer was correct!")
        else:
            self.change_text(
                self.feedback_box,
                "You're answer is incorrect. "
                "Please try again or skip the question.\n\n"
                '{}'.format(message)
            )

    def show_results(self):
        self.change_text(self.results_box, self.quiz.get_results())

    def change_text(self, widget, text):
        widget.configure(state='normal')
        widget.delete('1.0', Tkinter.END)
        widget.insert(Tkinter.END, text)
        widget.configure(state='disabled')


def main():
    root = Tkinter.Tk()
    tk_app = TkApp(root)
    root.mainloop()
    print(tk_app.quiz.get_results())


if __name__ == "__main__":
    main()
