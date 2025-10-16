# identifier/views.py
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Tree

# --- 질문 순서 정의 ---
QUESTIONS = [
    {'col': 'leaf_shape_overall', 'q': '잎의 전체적인 모양이 침엽인가요, 활엽인가요?'},
    {'col': 'form', 'q': '잎의 형태는 어떤가요?'},
    {'col': 'leaf_shape_detail', 'q': '잎이 생긴 모양은 어떤가요?'},
    {'col': 'leaf_length', 'q': '잎의 길이는 어느 정도인가요?'},
    {'col': 'leaf_arrangement', 'q': '잎이 나는 모양은 어떤가요?'},
    {'col': 'leaf_margin', 'q': '잎 가장자리는 어떤가요?'},
    {'col': 'leaf_margin_detail', 'q': '잎 가장자리의 생김새는 어떤가요?'}
]

CONIFER_QUESTIONS = [ # 침엽수 추가 질문
    {'col': 'sting_feel', 'q': '잎에 찔렸을 때 느낌은 어떤가요?'}
]

BROADLEAF_QUESTIONS = [ # 활엽수 추가 질문
    {'col': 'special_notes', 'q': '잎의 특이사항이 있나요?'},
    {'col': 'leaf_tip', 'q': '잎끝 모양은 어떤가요?'},
    {'col': 'petiole', 'q': '잎자루의 특징은 어떤가요?'},
    {'col': 'vein', 'q': '잎맥의 형태는 어떤가요?'},
    {'col': 'height', 'q': '나무의 키는 어느 정도인가요?'},
    {'col': 'fruit_flower', 'q': '열매나 꽃의 특징이 있나요?'}
]

def get_dynamic_questions(request):
    """URL 파라미터를 기반으로 동적 질문 목록을 생성합니다."""
    questions = QUESTIONS.copy()
    leaf_type = request.GET.get('leaf_shape_overall')
    if leaf_type == '침엽':
        questions.extend(CONIFER_QUESTIONS)
    elif leaf_type == '활엽':
        questions.extend(BROADLEAF_QUESTIONS)
    return questions

def index(request):
    """시작 페이지를 보여줍니다."""
    return render(request, 'index.html', {'start_page': True})

def restart(request):
    """처음으로 리디렉션합니다."""
    return redirect('index')

def question(request):
    """질문을 찾거나 결과를 보여줍니다."""
    # URL의 GET 파라미터를 사용하여 데이터베이스를 필터링합니다.
    queryset = Tree.objects.all()
    query_params = request.GET.copy()

    for key, value in query_params.items():
        if hasattr(Tree, key):
            # 복합적인 값을 가질 수 있는 필드는 '포함' 검색, 나머지는 '일치' 검색
            if key in ['leaf_shape_detail', 'form']:
                queryset = queryset.filter(**{f'{key}__icontains': value})
            else:
                queryset = queryset.filter(**{key: value})

    # 현재 답변 상태에 맞는 전체 질문 목록을 가져옵니다.
    all_questions = get_dynamic_questions(request)
    answered_cols = request.GET.keys()

    for q_info in all_questions:
        col = q_info['col']
        if col not in answered_cols:
            # 다음 질문의 선택지를 데이터베이스에서 직접 가져옵니다.
            # '잎이 생긴 모양'은 '/'로 분리하여 선택지 생성
            if col == 'leaf_shape_detail':
                all_options = set()
                db_values = queryset.values_list(col, flat=True).distinct()
                for item in db_values:
                    if item:
                        all_options.update(item.split('/'))
                options = sorted(list(all_options))
            else:
                options = sorted(list(queryset.values_list(col, flat=True).distinct()))
                options = [opt for opt in options if opt] # 빈 값 제거

            if len(options) >= 2:
                # 다음 질문을 찾았으면, 질문 페이지를 렌더링합니다.
                # 다음 답변을 추가할 URL을 미리 준비합니다.
                next_params = query_params.copy()
                context = {
                    'question': q_info['q'],
                    'options': options,
                    'next_params': next_params,
                    'next_col_name': col,
                }
                return render(request, 'index.html', context)

    # 더 이상 질문이 없으면, 최종 결과를 보여줍니다.
    results = list(queryset.values('sujong', 'gwa').distinct())
    return render(request, 'index.html', {'results': results})
