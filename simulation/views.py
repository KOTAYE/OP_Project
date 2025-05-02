from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
import uuid

# Симуляційні блоки
# Симуляційні блоки
SIMULATION_BLOCKS = [
    {
        "id": 1,
        "title": "Придатність до нормального сну",
        "description": "Перевірка базових факторів, що впливають на якість сну",
        "questions": [
            {"id": 1, "text": "Скільки годин ви спите щодня?", "score": 1, "answers": [
                {"id": 1, "text": "Менше 5 годин", "is_correct": False},
                {"id": 2, "text": "Від 5 до 7 годин", "is_correct": True},
                {"id": 3, "text": "Більше 7 годин", "is_correct": True}
            ]},
            {"id": 2, "text": "Чи часто ви прокидаєтесь вночі?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 3, "text": "Чи маєте ви проблеми із засинанням?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 4, "text": "Чи використовуєте ви гаджети перед сном?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 5, "text": "Чи відчуваєте ви себе відпочилим після сну?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 6, "text": "Чи маєте ви стреси або тривоги, які впливають на сон?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 7, "text": "Чи відчуваєте ви вночі біль або дискомфорт?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 8, "text": "Чи відчуваєте ви сонливість вдень?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]}
        ]
    },
    {
        "id": 2,
        "title": "Медичні фактори сну",
        "description": "Симуляція аналізу медичних показників для нормалізації сну",
        "questions": [
            {"id": 9, "text": "Чи є у вас проблеми з диханням під час сну?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 10, "text": "Чи є у вас порушення серцевого ритму під час сну?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 11, "text": "Чи страждаєте ви від безсоння?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 12, "text": "Чи маєте ви проблеми з температурою тіла під час сну?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 13, "text": "Чи маєте ви хронічні захворювання, що впливають на ваш сон?", "score": 1, "answers": [
                {"id": 1, "text": "Ні", "is_correct": True},
                {"id": 2, "text": "Так", "is_correct": False}
            ]},
            {"id": 14, "text": "Чи маєте ви депресію або тривожність, що заважають нормальному сну?", "score": 1, "answers": [
                {"id": 1, "text": "Ні", "is_correct": True},
                {"id": 2, "text": "Так", "is_correct": False}
            ]},
            {"id": 15, "text": "Чи є у вас алергії, що впливають на якість сну?", "score": 1, "answers": [
                {"id": 1, "text": "Ні", "is_correct": True},
                {"id": 2, "text": "Так", "is_correct": False}
            ]},
            {"id": 16, "text": "Чи спостерігаєте ви себе з порушеннями слуху під час сну?", "score": 1, "answers": [
                {"id": 1, "text": "Ні", "is_correct": True},
                {"id": 2, "text": "Так", "is_correct": False}
            ]}
        ]
    },
    {
        "id": 3,
        "title": "Звички та умови для хорошого сну",
        "description": "Аналіз ваших звичок і умов для досягнення хорошого сну",
        "questions": [
            {"id": 17, "text": "Чи маєте ви регулярний графік сну?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 18, "text": "Чи вживаєте ви каву або енергетики перед сном?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": False},
                {"id": 2, "text": "Ні", "is_correct": True}
            ]},
            {"id": 19, "text": "Чи спите ви в затемненій кімнаті?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 20, "text": "Чи займаєтесь ви фізичними вправами протягом дня?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 21, "text": "Чи не працюєте ви за комп'ютером або не використовуєте гаджети перед сном?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 22, "text": "Чи маєте ви зручну постіль для сну?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 23, "text": "Чи спите ви у комфортній температурі?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]},
            {"id": 24, "text": "Чи спите ви в тиші без сторонніх шумів?", "score": 1, "answers": [
                {"id": 1, "text": "Так", "is_correct": True},
                {"id": 2, "text": "Ні", "is_correct": False}
            ]}
        ]
    }
]

# Усі інші функції залишаються незмінними

# ==== UTILS ====

def get_all_questions(block_id=None):
    """Get questions from all blocks or a specific block"""
    questions = []
    for block in SIMULATION_BLOCKS:
        if block_id and block["id"] != block_id:
            continue
        for question in block["questions"]:
            question_with_block = question.copy()
            question_with_block["block_id"] = block["id"]
            question_with_block["block_title"] = block["title"]
            questions.append(question_with_block)
    return questions

def get_question_by_id(question_id, block_id=None):
    all_questions = get_all_questions(block_id)
    return next((q for q in all_questions if q["id"] == question_id), None)

def get_next_question_id(current_question_id, block_id):
    all_questions = get_all_questions(block_id)
    for i, question in enumerate(all_questions):
        if question["id"] == current_question_id and i < len(all_questions) - 1:
            return all_questions[i + 1]["id"]
    return None

def calculate_total_score(user_answers, block_id):
    questions = get_all_questions(block_id)
    total_score = 0
    max_score = sum(q["score"] for q in questions)
    for question in questions:
        answer_id = user_answers.get(str(question["id"]))
        if answer_id:
            for ans in question["answers"]:
                if ans["id"] == answer_id and ans["is_correct"]:
                    total_score += question["score"]
                    break
    return total_score, max_score

def get_result_text(score, simulation_id):
    if simulation_id == 1:
        if score == 3:
            return "Ваші відповіді свідчать про загалом здоровий режим сну. Ви адаптовані до регулярного, відновлювального відпочинку."
        elif score == 2:
            return "У вас є деякі труднощі зі сном, але ситуація не критична. Рекомендується звернути увагу на стабільність режиму."
        else:
            return "Ваш режим сну, ймовірно, порушений. Рекомендується оцінити звички й обов’язково звернутися до спеціаліста."

    elif simulation_id == 2:
        if score == 3:
            return "Наразі немає очевидних медичних факторів, що негативно впливають на ваш сон."
        elif score == 2:
            return "Можливі незначні медичні фактори, які варто контролювати. Рекомендується консультація зі спеціалістом."
        else:
            return "Існують медичні причини, які можуть серйозно впливати на ваш сон. Важливо пройти обстеження."

    elif simulation_id == 3:
        if score == 3:
            return "Ваші звички й умови сприяють глибокому та якісному сну. Продовжуйте в тому ж дусі!"
        elif score == 2:
            return "Умови сну задовільні, але є потенціал для покращення. Зверніть увагу на світло, шум і гігієну сну."
        else:
            return "Ваше оточення або звички можуть заважати повноцінному відпочинку. Варто переглянути обстановку й режим."

    return "Результат недоступний для цієї симуляції."


# ==== VIEWS ====

def start_simulation(request):
    block_id = request.GET.get('block_id')
    if not block_id:
        return render(request, 'simulation/start.html', {'blocks': SIMULATION_BLOCKS})

    block_id = int(block_id)
    questions = get_all_questions(block_id)
    if not questions:
        return render(request, 'simulation/no_blocks.html')

    simulation_data = {
        'id': str(uuid.uuid4()),
        'start_time': timezone.now().isoformat(),
        'current_question': questions[0]['id'],
        'answers': {},
        'selected_block_id': block_id
    }

    request.session['simulation'] = simulation_data
    return redirect('simulation:question', question_id=questions[0]['id'])

def show_question(request, question_id):
    question_id = int(question_id)
    if 'simulation' not in request.session:
        return redirect('simulation:start')

    simulation = request.session['simulation']
    block_id = simulation.get('selected_block_id')
    question = get_question_by_id(question_id, block_id)

    if not question:
        raise Http404("Питання не знайдено")

    if request.method == 'POST':
        selected_answer_id = int(request.POST.get('answer', 0))
        simulation['answers'][str(question_id)] = selected_answer_id
        request.session['simulation'] = simulation

        next_id = get_next_question_id(question_id, block_id)
        if next_id:
            return redirect('simulation:question', question_id=next_id)
        else:
            return redirect('simulation:results')

    all_questions = get_all_questions(block_id)
    current_index = next((i for i, q in enumerate(all_questions) if q["id"] == question_id), 0)

    context = {
        'question': question,
        'total_questions': len(all_questions),
        'current_question_number': current_index + 1
    }
    return render(request, 'simulation/question.html', context)

def show_result(request):
    if 'simulation' not in request.session:
        return redirect('simulation:start')

    simulation = request.session['simulation']
    block_id = simulation.get('selected_block_id')
    answers = simulation.get('answers', {})

    score, max_score = calculate_total_score(answers, block_id)
    result_text = get_result_text(score, block_id)

    context = {
        'score': score,
        'max_score': max_score,
        'result_text': result_text
    }
    return render(request, 'simulation/results.html', context)
