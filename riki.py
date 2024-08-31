  import pandas as pd
      import random
      from pyodide.http import open_url
      from pyscript import Element

      # スコアと問題カウントを追跡する変数
      score = 0
      question_count = 0
      total_questions = 10
      incorrect_questions = []  # 間違えた問題を保存するリスト

      def read_csv(filepath):
        df = pd.read_csv(open_url(filepath))
        data = df.values.tolist()
        return data
      
      def random_quiz(max_num, content):
        randomnum = random.randint(0, max_num - 1)
        quiz = content[randomnum]
        return quiz

      def load_quiz():
        global correct_option, question_count, current_question
        # 問題カウントをチェック
        if question_count >= total_questions:
            show_final_score()
            return
        
        quiz = random_quiz(max_num, content)
        current_question = quiz[0]  # 現在の問題を保存
        correct_option = quiz[1]
        options = [quiz[2], quiz[3], quiz[4], quiz[5]]
        random.shuffle(options)
    
        # 問題とスコアの表示を更新
        pyscript.write("lb", current_question)
        pyscript.write("status", f"第 {question_count + 1} 問目 (スコア: {score} / {total_questions})")

        form = Element("radioForm")
        form.element.innerHTML = ""
        for option in options:
            new_radio = f'<label><input type="radio" name="option" value="{option}"> {option}</label><br>'
            form.element.innerHTML += new_radio

      def check_answer(event=None):
        global score, question_count
        selected_option = None
        form = Element("radioForm")
        for radio in form.element.querySelectorAll('input[name="option"]'):
            if radio.checked:
                selected_option = radio.value
                break

        result = Element("result")
        if selected_option == correct_option:
            score += 1
            result.element.innerHTML = "正解です！次の問題に進みます。"
        else:
            result.element.innerHTML = "不正解です。もう一度挑戦してください。"
            incorrect_questions.append((current_question, correct_option))  # 間違えた問題と正解を保存

        question_count += 1
        load_quiz()

      def show_final_score():
        result = Element("result")
        result.element.innerHTML = f"クイズ終了！あなたのスコアは {score} / {total_questions} です。<br><br>"

        if incorrect_questions:
            result.element.innerHTML += "間違えた問題と正解:<br>"
            for question, correct in incorrect_questions:
                result.element.innerHTML += f"問題: {question}<br>正解: {correct}<br><br>"

        # 「もう一回行いますか？」ボタンを表示
        restart_btn = Element("restartBtn")
        restart_btn.element.style.display = "block"

      def reset_quiz(event=None):
        global score, question_count, incorrect_questions
        score = 0
        question_count = 0
        incorrect_questions = []

        # 表示をリセット
        pyscript.write("result", "")
        pyscript.write("status", "")
        Element("restartBtn").element.style.display = "none"

        # 新しいクイズを開始
        load_quiz()

      filepath = "https://raw.githubusercontent.com/taisei1223/create_game/main/onepice.csv"
      content = read_csv(filepath)

      max_num = len(content)

      load_quiz()

      submit_btn = Element("submitBtn")
      submit_btn.element.onclick = check_answer

      # リセットボタンのイベントリスナーを追加
      restart_btn = Element("restartBtn")
      restart_btn.element.onclick = reset_quiz

