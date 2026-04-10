import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pingouin as pg
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import r2_score
import networkx as nx
import io
# !!!ЗАПУСК: streamlit run dashboard_Pro.py
# ==========================================
# МОДУЛЬ СПРАВКИ (Всплывающее окно)
# ==========================================
@st.dialog("📖 Справочное руководство", width="large")
def show_help_dialog():
    menu_col, content_col = st.columns([1, 2.5])
    
    with menu_col:
        st.markdown("**Разделы:**")
        selected_topic = st.radio(
            "Навигация по справке",
            [
                "📥 Загрузка и Фильтры",
                "📊 Обзор выборки",
                "🧩 Анализ методик",
                "🆚 Сравнение групп",
                "🔗 Корреляции",
                "🔬 Кластеры и Качество",
                "🔮 Поиск драйверов",
                "👽 Детектор аномалий",
                "🕸️ Сетевой анализ"
            ],
            label_visibility="collapsed"
        )
        
    with content_col:
        if selected_topic == "📥 Загрузка и Фильтры":
            st.markdown("### 📥 Загрузка данных и Фильтрация")
            st.info("💡 **Основной принцип:** Любые изменения в левой боковой панели автоматически пересчитывают данные на всех вкладках дашборда.")
            
            st.markdown("**Пошаговая инструкция:**")
            st.markdown("""
            1. **Загрузка файла:** Перетащите файл Excel (`.xlsx`) в поле `Drag and drop file here` в левом меню.
            2. **Настройка фильтров:** Выберите нужные параметры (например, Пол: *Мужской*, Возраст: *18-25*). Можно оставить поля пустыми, чтобы анализировать всех.
            3. **Применение:** Нажмите синюю кнопку **«Применить фильтры»**.
            4. **Выгрузка:** Чтобы скачать отфильтрованную таблицу для работы в других программах, нажмите **«📥 Скачать отфильтрованные данные»** в самом низу панели.
            """)
            
        elif selected_topic == "📊 Обзор выборки":
            st.markdown("### 📊 Вкладка 1: Обзор выборки")
            st.markdown("Раздел для анализа социально-демографического состава и распределения баллов.")
            
            st.markdown("**Доступные инструменты:**")
            st.markdown("""
            * **Конструктор демографии:** Выберите признак из выпадающего списка, чтобы построить круговую или столбчатую диаграмму.
            * **Анализ распределений:** * *Скрипичный график (Violin):* Показывает плотность ответов. Широкая часть — там, где ответов больше всего.
              * *Ящик с усами (Boxplot):* Точка в центре — медиана. Границы ящика — основная масса людей (50%). Точки за усами — выбросы.
            * **Кросс-табуляция:** Выберите два признака (Строки и Колонки), чтобы получить сводную таблицу (например, распределение семейного положения по полу).
            """)
            
        elif selected_topic == "🧩 Анализ методик":
            st.markdown("### 🧩 Вкладка 2: Анализ методик")
            st.markdown("Детальный разбор психологических шкал.")
            
            st.warning("⚡ **Режимы работы:** Вверху страницы выберите, чьи данные вы хотите видеть: всей группы (средние значения) или конкретного человека (выбор по ФИО/ID).")
            
            st.markdown("**Как читать графики (на примере Мильмана):**")
            st.markdown("""
            * **Зеленая линия:** Желаемое (Идеал).
            * **Красная линия:** Действительное (Реальность).
            * **Разрыв:** Чем дальше красная точка от зеленой на одной шкале, тем выше уровень неудовлетворенности (фрустрации) в этой сфере.
            """)
            
        elif selected_topic == "🆚 Сравнение групп":
            st.markdown("### 🆚 Вкладка 3: Сравнение групп")
            st.markdown("Автоматический поиск статистически значимых различий (p-value < 0.05).")
            
            st.info("⚙️ **Под капотом:** Система сама проверяет нормальность распределения и выбирает критерий (t-Стьюдента или U-Манна-Уитни).")
            
            st.markdown("**Инструкция:**")
            st.markdown("""
            1. Выберите **Группирующий признак** (например, Пол).
            2. Нажмите **«Найти значимые различия»**.
            3. **Результат:** Таблица покажет *только те шкалы*, по которым группы достоверно отличаются. Зеленым подсвечивается группа, у которой балл выше.
            """)
            
        elif selected_topic == "🔗 Корреляции":
            st.markdown("### 🔗 Вкладка 4: Корреляции")
            st.markdown("Поиск взаимосвязей между шкалами (от -1.0 до 1.0).")
            
            st.markdown("**Интерфейс:**")
            st.markdown("""
            * **Тепловая карта:** Красный цвет — отрицательная связь (одно растет, другое падает). Синий цвет — положительная связь.
            * **Фильтр связей (внизу):** 1. Выберите силу связи (например, `> 0.5` или `< -0.5`).
              2. Задайте уровень значимости (обычно `p < 0.05`).
              3. Получите чистую таблицу только с самыми сильными и надежными корреляциями.
            """)
            
        elif selected_topic == "🔬 Кластеры и Качество":
            st.markdown("### 🔬 Вкладки 5 и 6: Кластеры и Психометрика")
            
            st.markdown("**Вкладка 5: Кластерный анализ**")
            st.markdown("""
            Разделение людей на схожие типажи.
            * Выберите шкалы. Алгоритм K-Means сам предложит оптимальное количество кластеров.
            * Радарные диаграммы покажут профиль каждого кластера (чем отличается Группа 1 от Группы 2).
            """)
            
            st.markdown("**Вкладка 6: Психометрика**")
            st.markdown("""
            * **Альфа Кронбаха:** Метрика надежности теста. Норма > 0.7.
            * **Метод главных компонент (PCA):** Сжимает все шкалы в 2-3 крупных фактора и выводит таблицу "нагрузок" (какие шкалы вошли в состав каждого фактора).
            """)
            
        elif selected_topic == "🔮 Поиск драйверов":
            st.markdown("### 🔮 Вкладка 7: Поиск драйверов (Random Forest)")
            st.markdown("Определяет, какие факторы сильнее всего влияют на выбранный целевой показатель.")
            
            st.markdown("**Инструкция:**")
            st.markdown("""
            1. Выберите **Целевой показатель** (например, Общий балл ИПЛ).
            2. Выберите **Факторы влияния** (например, все шкалы Мильмана).
            3. Нажмите **«Найти драйверы»**.
            """)
            
            st.info("📈 **Катализатор:** Фактор повышает целевой показатель.\n📉 **Блокатор:** Фактор снижает целевой показатель.")
            
            st.markdown("**Симулятор «Что-если» (Внизу страницы):**")
            st.markdown("Двигайте ползунки найденных факторов и нажимайте «Пересчитать», чтобы увидеть прогноз изменения целевого показателя.")
            
        elif selected_topic == "👽 Детектор аномалий":
            st.markdown("### 👽 Вкладка 8: Детектор аномалий")
            st.markdown("Поиск респондентов с нетипичными профилями (выбросов).")
            
            st.markdown("**Инструкция:**")
            st.markdown("""
            1. Задайте чувствительность ползунком (рекомендуется 5%).
            2. Нажмите **«Найти аномалии»**. На графике красными точками будут отмечены нетипичные люди.
            3. В блоке **«Рентген аномалии»** выберите человека из списка.
            4. **Результат:** График (Z-score) покажет, какие именно баллы у этого человека аномально завышены (зеленый) или занижены (красный) по сравнению с остальной группой.
            """)
            
        elif selected_topic == "🕸️ Сетевой анализ":
            st.markdown("### 🕸️ Вкладка 9: Сетевая психометрия")
            st.markdown("Визуализация структуры мотивов в виде графа.")
            
            st.markdown("**Как читать граф:**")
            st.markdown("""
            * **Узлы (Кружки):** Шкалы теста. Чем больше кружок, тем больше у него связей (Центральный мотив).
            * **Линии:** Корреляции между шкалами. 
              * 🟢 **Зеленая:** Прямая связь (синхронность).
              * 🔴 **Красная:** Обратная связь (конфликт).
            * **Ползунок порога:** Если линий слишком много (каша), увеличьте порог отсечения (например, до 0.4), чтобы оставить только самые сильные связи.
            """)
            st.info("💾 Внизу страницы есть кнопка скачивания графа в формате интерактивного HTML-файла.")
# ==========================================
# ГЛОБАЛЬНЫЙ СЛОВАРЬ РАСШИФРОВКИ ШКАЛ
# ==========================================
SCALE_NAMES_RU = {
    # Демография
    'Age': 'Возраст',
    'Course': 'Курс',
    # Братусь
    'B_Altruistic': 'Братусь: Альтруистические',
    'B_Existential': 'Братусь: Экзистенциальные',
    'B_Hedonistic': 'Братусь: Гедонистические',
    'B_Self-realization': 'Братусь: Самореализации',
    'B_Status': 'Братусь: Статусные',
    'B_Communicative': 'Братусь: Коммуникативные',
    'B_Family': 'Братусь: Семейные',
    'B_Cognitive': 'Братусь: Когнитивные',
    
    # Мильман (Жизнь - Идеал/Реал)
    'M_P_Zh-id': 'Мильман: Поддержание (Жизнь, Идеал)',
    'M_P_Zh-re': 'Мильман: Поддержание (Жизнь, Реал)',
    'M_K_Zh-id': 'Мильман: Комфорт (Жизнь, Идеал)',
    'M_K_Zh-re': 'Мильман: Комфорт (Жизнь, Реал)',
    'M_S_Zh-id': 'Мильман: Статус (Жизнь, Идеал)',
    'M_S_Zh-re': 'Мильман: Статус (Жизнь, Реал)',
    'M_O_Zh-id': 'Мильман: Общение (Жизнь, Идеал)',
    'M_O_Zh-re': 'Мильман: Общение (Жизнь, Реал)',
    'M_D_Zh-id': 'Мильман: Активность (Жизнь, Идеал)',
    'M_D_Zh-re': 'Мильман: Активность (Жизнь, Реал)',
    'M_DR_Zh-id': 'Мильман: Творчество (Жизнь, Идеал)',
    'M_DR_Zh-re': 'Мильман: Творчество (Жизнь, Реал)',
    'M_OD_Zh-id': 'Мильман: Общ. польза (Жизнь, Идеал)',
    'M_OD_Zh-re': 'Мильман: Общ. польза (Жизнь, Реал)',
    
    # Мильман (Работа - Идеал/Реал)
    'M_P_Rb-id': 'Мильман: Поддержание (Работа, Идеал)',
    'M_P_Rb-re': 'Мильман: Поддержание (Работа, Реал)',
    'M_K_Rb-id': 'Мильман: Комфорт (Работа, Идеал)',
    'M_K_Rb-re': 'Мильман: Комфорт (Работа, Реал)',
    'M_S_Rb-id': 'Мильман: Статус (Работа, Идеал)',
    'M_S_Rb-re': 'Мильман: Статус (Работа, Реал)',
    'M_O_Rb-id': 'Мильман: Общение (Работа, Идеал)',
    'M_O_Rb-re': 'Мильман: Общение (Работа, Реал)',
    'M_D_Rb-id': 'Мильман: Активность (Работа, Идеал)',
    'M_D_Rb-re': 'Мильман: Активность (Работа, Реал)',
    'M_DR_Rb-id': 'Мильман: Творчество (Работа, Идеал)',
    'M_DR_Rb-re': 'Мильман: Творчество (Работа, Реал)',
    'M_OD_Rb-id': 'Мильман: Общ. польза (Работа, Идеал)',
    'M_OD_Rb-re': 'Мильман: Общ. польза (Работа, Реал)',

    # Мильман (Эмоции)
    'M_Est': 'Мильман: Стенические',
    'M_East': 'Мильман: Астенические',
    'M_Fst': 'Мильман: Стенические (Фрустрация)',
    'M_Fast': 'Мильман: Астенические (Фрустрация)',

    # ИПЛ
    'IPL_Total': 'ИПЛ: Общий балл',
    'IPL_G': 'ИПЛ: Гносеологический (Г)',
    'IPL_A': 'ИПЛ: Аксиологический (А)',
    'IPL_P': 'ИПЛ: Праксеологический (П)',
    'IPL_Type_OI': 'ИПЛ: Осмысленно-интенсивный (ОИ)',
    'IPL_Type_FN': 'ИПЛ: Формально-накопительский (ФН)',
    'IPL_Type_PD': 'ИПЛ: Позитивно-дифференцированный (ПД)',
    'IPL_Type_NG': 'ИПЛ: Негативно-генерализованный (НГ)',
    'IPL_Type_IP': 'ИПЛ: Инициативно-преобразовательный (ИП)',
    'IPL_Type_VP': 'ИПЛ: Вынужденно-приспособительный (ВП)',
    'IPL_Level_Nature': 'ИПЛ: Природный уровень',
    'IPL_Level_Social': 'ИПЛ: Социальный уровень',
    'IPL_Level_Culture': 'ИПЛ: Культурный уровень',
    'IPL_Level_Life': 'ИПЛ: Уровень жизни'
}

def get_name(col):
    """Функция возвращает русское название шкалы или оригинальное, если перевода нет"""
    return SCALE_NAMES_RU.get(col, col)
# ==========================================
# ==========================================
# 1. НАСТРОЙКА СТРАНИЦЫ И КОНФИГУРАЦИЯ
# ==========================================
st.set_page_config(page_title="Анализ Психодиагностики Pro", layout="wide", page_icon="🧠")

# ==========================================
# 2. ЯДРО АНАЛИТИКИ (ФУНКЦИИ РАСЧЕТА)
# ==========================================

@st.cache_data(ttl=3600)
def load_data(file):
    """Загрузка данных с кэшированием."""
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки файла: {e}")
        return None

def get_descriptive_stats(df, columns):
    """Считает описательную статистику и нормальность распределения."""
    stats_list = []
    for col in columns:
        if col not in df.columns: continue
        series = df[col].dropna()
        if len(series) < 3: continue # Слишком мало данных

        desc = series.describe()
        # Тест на нормальность (Shapiro-Wilk)
        try:
            normality = pg.normality(series)
            p_val = normality['pval'].values[0]
            is_normal = p_val > 0.05
        except:
            p_val = 0
            is_normal = False

        stats_list.append({
            "Показатель": col,
            "N": int(desc['count']),
            "Среднее": desc['mean'],
            "SD": desc['std'],
            "Медиана": desc['50%'],
            "Min": desc['min'],
            "Max": desc['max'],
            "Skew": series.skew(),
            "Kurtosis": series.kurtosis(),
            "Нормальность (p)": f"{p_val:.3f} ({'Да' if is_normal else 'Нет'})"
        })
    return pd.DataFrame(stats_list)

def smart_compare_groups(df, group_col, metric_col):
    """
    Автоматически выбирает тест в зависимости от кол-ва групп и нормальности распределения.
    Параметрические: T-test (Welch), ANOVA.
    Непараметрические: Mann-Whitney U, Kruskal-Wallis.
    """
    clean_df = df[[group_col, metric_col]].dropna()
    groups = clean_df[group_col].unique()
    
    if len(groups) < 2:
        return None, "Меньше 2 групп"
    
    try:
        # 1. Быстрая проверка на нормальность (Shapiro-Wilk)
        # Если хотя бы в одной подгруппе распределение ненормальное (p < 0.05), переходим на непараметрику
        is_normal = True
        for g in groups:
            g_data = clean_df[clean_df[group_col] == g][metric_col]
            if len(g_data) >= 3:
                stat = pg.normality(g_data)
                if stat['pval'].values[0] < 0.05:
                    is_normal = False
                    break

        # 2. Выбор и проведение теста
        if len(groups) == 2:
            g1 = clean_df[clean_df[group_col] == groups[0]][metric_col]
            g2 = clean_df[clean_df[group_col] == groups[1]][metric_col]
            
            if is_normal:
                res = pg.ttest(g1, g2, correction=True) # Welch's T-test
                test_name = "T-test (Welch)"
                p_val = res['p-val'].values[0]
                eff_size = res['cohen-d'].values[0]
                eff_label = "Cohen's d"
            else:
                res = pg.mwu(g1, g2) # Mann-Whitney
                test_name = "Mann-Whitney U (Непараметрический)"
                p_val = res['p-val'].values[0]
                eff_size = res['RBC'].values[0] # Rank-Biserial Correlation
                eff_label = "Rank-Biserial"
                
        else:
            if is_normal:
                res = pg.anova(data=clean_df, dv=metric_col, between=group_col)
                test_name = "One-way ANOVA"
                p_val = res['p-unc'].values[0]
                eff_size = res['np2'].values[0]
                eff_label = "Eta-sq (η²)"
            else:
                res = pg.kruskal(data=clean_df, dv=metric_col, between=group_col)
                test_name = "Kruskal-Wallis (Непараметрический)"
                p_val = res['p-unc'].values[0]
                eff_size = res['H'].values[0] # H-статистика
                eff_label = "H-stat"

        # 3. Интерпретация значимости
        stars = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else ""))
        
        result_df = pd.DataFrame({
            "Метрика": [metric_col],
            "Тест": [test_name],
            "p-value": [f"{p_val:.4f} {stars}"],
            f"Эффект ({eff_label})": [f"{eff_size:.3f}"]
        })
        return result_df, p_val
        
    except Exception as e:
        return None, str(e)

def run_clustering_analysis(df, cols, n_clusters):
    """Выполняет PCA и K-Means кластеризацию."""
    data = df[cols].dropna()
    if data.empty: return None
    
    # Масштабирование
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    # Кластеризация
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(data_scaled)
    
    # PCA для визуализации (2D)
    pca = PCA(n_components=2)
    components = pca.fit_transform(data_scaled)
    
    # Сборка результата
    res_df = data.copy()
    res_df['Cluster'] = clusters.astype(str)
    res_df['PC1'] = components[:, 0]
    res_df['PC2'] = components[:, 1]
    
    # Добавляем ID или другие метаданные из исходного df если нужно, по индексу
    res_df = res_df.join(df[['Gender', 'Age']], how='left')
    
    return res_df

# ==========================================
# 3. ИНТЕРФЕЙС И ЗАГРУЗКА
# ==========================================

st.title("🧠 Аналитическая система: Психодиагностика v3.0")

# --- САЙДБАР: ЗАГРУЗКА И ФИЛЬТРЫ ---
with st.sidebar:
    if st.button("📖 Открыть руководство", use_container_width=True, type="primary"):
        show_help_dialog()
    st.header("1. Данные")
    uploaded_file = st.file_uploader("Загрузить XLSX", type=['xlsx'])
    
    df_raw = None
    if uploaded_file:
        df_raw = load_data(uploaded_file)
    else:
        # Попытка найти локальный файл
        try:
            df_raw = load_data('FINAL_RESULTS.xlsx')
            st.success("✅ Загружен локальный файл")
        except:
            pass

    if df_raw is None:
        st.warning("Ожидание файла...")
        st.stop()

    st.markdown("---")
    st.header("2. Фильтры")
    
    with st.form("filters_form"):
        st.subheader("Параметры фильтрации")
        
        # 1. Пол
        all_genders = sorted(df_raw['Gender'].dropna().astype(str).unique().tolist())
        sel_gender = st.multiselect("Пол", all_genders, default=all_genders)
        
        # 2. Возраст
        min_a, max_a = int(df_raw['Age'].min()), int(df_raw['Age'].max())
        if min_a < max_a:
            sel_age = st.slider("Возраст", min_a, max_a, (min_a, max_a))
        else:
            sel_age = (min_a, max_a)
            st.info(f"Возраст всех респондентов: {min_a}")
            
        # 3. Работа
        all_work = sorted(df_raw['Work'].dropna().astype(str).unique().tolist())
        sel_work = st.multiselect("Работа", all_work, default=all_work)

        # 4. Образование 
        if 'Edu_Status' in df_raw.columns:
            all_edu = sorted(df_raw['Edu_Status'].dropna().astype(str).unique().tolist())
            sel_edu = st.multiselect("Образование", all_edu, default=all_edu)
        else:
            sel_edu = []

        # 5. КМНС 
        sel_kmns = []
        if 'Is_KMNS' in df_raw.columns:
            all_kmns = sorted(df_raw['Is_KMNS'].dropna().astype(str).unique().tolist())
            sel_kmns = st.multiselect("Относится к КМНС?", all_kmns, default=all_kmns)
# --- НОВЫЙ БЛОК: ДОПОЛНИТЕЛЬНЫЕ ФИЛЬТРЫ ---
        with st.expander("Дополнительные фильтры", expanded=False):
            # Список новых полей для фильтрации
            extra_cols = {
                'KMNS_Name': 'Конкретный народ (КМНС)',
                'Family': 'Семейное положение',
                'Children': 'Наличие детей',
                'University': 'Название ВУЗа',
                'Speciality': 'Специальность',
                'Edu_Level': 'Уровень обучения',
                'Edu_Basis': 'Основа обучения'
            }
            
            sel_extra = {}
            for col, label in extra_cols.items():
                if col in df_raw.columns:
                    options = sorted(df_raw[col].dropna().astype(str).unique().tolist())
                    sel_extra[col] = st.multiselect(label, options, default=options)
                else:
                    sel_extra[col] = [] # Если колонки нет в Excel, фильтр просто не сработает
        submit = st.form_submit_button("Применить фильтры")


# Логика применения фильтров
# Сначала формируем маску для основных полей
mask = (
    (df_raw['Gender'].astype(str).isin(sel_gender)) &
    (df_raw['Age'].between(sel_age[0], sel_age[1])) &
    (df_raw['Work'].astype(str).isin(sel_work))
)

# Применяем фильтр по Образованию, если он есть
if 'Edu_Status' in df_raw.columns and sel_edu:
    mask = mask & (df_raw['Edu_Status'].astype(str).isin(sel_edu))

# Применяем фильтр по КМНС, если он есть
if 'Is_KMNS' in df_raw.columns and sel_kmns:
    mask = mask & (df_raw['Is_KMNS'].astype(str).isin(sel_kmns))
# Дополняем маску новыми фильтрами из sel_extra
for col, selected in sel_extra.items():
    if col in df_raw.columns and selected:
        mask = mask & (df_raw[col].astype(str).isin(selected))
# Применяем итоговую маску
df = df_raw[mask].copy()


st.sidebar.markdown("---")
st.sidebar.metric("Выборка", f"{len(df)} чел.", delta=len(df)-len(df_raw))
# --- НОВЫЙ КОД: КНОПКА СКАЧИВАНИЯ ВЫБОРКИ (EXCEL) ---
buffer = io.BytesIO()
df.to_excel(buffer, index=False, engine='openpyxl')
    
st.sidebar.download_button(
        label="📥 Скачать текущую выборку (Excel)",
        data=buffer.getvalue(),
        file_name='filtered_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="Скачать сырые данные в формате Excel с учетом примененных фильтров"
    )
    # --- КОНЕЦ НОВОГО КОДА ---
# ==========================================
# 4. ОСНОВНОЙ КОНТЕНТ (ВКЛАДКИ)
# ==========================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Обзор выборки", 
    "🧩 Методики", 
    "🆚 Сравнение групп", 
    "🔗 Корреляции", 
    "🔬 Кластерный анализ",
    "📐 Психометрика",
    "🔮 Поиск драйверов",
    "👽 Поиск аномалий",
    "🕸️ Сетевой анализ личности"
])
# === TAB 1: ОБЗОР ВЫБОРКИ ===
with tab1:
    st.header("Обзор выборки")

    # --- 1. ПАНЕЛЬ БЫСТРЫХ KPI ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_n = len(df)
    mean_age = df['Age'].mean() if 'Age' in df.columns else 0
    
    # Преобладающий пол
    if 'Gender' in df.columns and not df['Gender'].empty:
        top_gender = df['Gender'].mode()[0]
        top_gender_pct = (df['Gender'] == top_gender).sum() / total_n * 100
        gender_text = f"{top_gender} ({top_gender_pct:.0f}%)"
    else:
        gender_text = "Н/Д"
        
    # Процент работающих (считаем долю ответов "Да" в колонке Work, если она есть)
    if 'Work' in df.columns and not df['Work'].empty:
        working_pct = (df['Work'].astype(str).str.contains('Да', case=False, na=False)).sum() / total_n * 100
        work_text = f"{working_pct:.0f}%"
    else:
        work_text = "Н/Д"

    kpi1.metric("👥 Всего респондентов", f"{total_n} чел.")
    kpi2.metric("🎂 Средний возраст", f"{mean_age:.1f} лет")
    kpi3.metric("⚧ Преобладающий пол", gender_text)
    kpi4.metric("💼 Работающих", work_text)
    
    st.markdown("---")

    # Создаем под-вкладки для структуры
    tab1_demo, tab1_stats, tab1_cross = st.tabs([
        "👥 Социально-демографический портрет", 
        "📈 Статистика и Распределения", 
        "🔀 Кросс-табуляция (Срезы)"
    ])

    with tab1_demo:
        st.subheader("Социально-демографическая структура")
        
        c1, c2 = st.columns([1, 1.2]) # Правая колонка чуть шире для удобства настроек
        
        # --- СТАТИЧНЫЙ БЛОК: ВОЗРАСТ ---
        with c1:
            st.markdown("#### Возрастной состав")
            if 'Age' in df.columns:
                fig_age = px.histogram(df, x='Age', nbins=15, color_discrete_sequence=['#3498db'])
                fig_age.update_layout(yaxis_title="Количество чел.", xaxis_title="Возраст", margin=dict(t=20, b=10))
                st.plotly_chart(fig_age, use_container_width=True)
            else:
                st.info("Данные о возрасте отсутствуют.")
                
        # --- ИНТЕРАКТИВНЫЙ БЛОК: КОНСТРУКТОР ---
        with c2:
            st.markdown("#### Конструктор демографии")
            
            # Словарь всех возможных категорий для перевода на русский
            demo_dict = {
                'Gender': 'Пол',
                'Family': 'Семейное положение',
                'Children': 'Наличие детей',
                'Work': 'Трудоустройство',
                'Edu_Status': 'Статус обучения',
                'Edu_Level': 'Уровень образования',
                'Is_KMNS': 'Принадлежность к КМНС'
            }
            # Оставляем только те колонки, которые реально есть в текущем Excel-файле
            available_demo = {k: v for k, v in demo_dict.items() if k in df.columns}
            
            if available_demo:
                # Меню настроек графика
                col_sel1, col_sel2 = st.columns(2)
                with col_sel1:
                    sel_var = st.selectbox("1. Показатель:", list(available_demo.keys()), format_func=lambda x: available_demo[x])
                with col_sel2:
                    sel_viz = st.selectbox("2. Вид графика:", [
                        "Круговая диаграмма (Pie)", 
                        "Вертикальные столбцы (Bar)", 
                        "Горизонтальные столбцы (Bar)", 
                        "Древовидная карта (Treemap)"
                    ])
                
                # Подготовка данных для выбранного показателя
                var_counts = df[sel_var].value_counts().reset_index()
                var_counts.columns = ['Категория', 'Количество']
                
                # Отрисовка выбранного типа графика
                if sel_viz == "Круговая диаграмма (Pie)":
                    fig_dyn = px.pie(var_counts, names='Категория', values='Количество', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig_dyn.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
                    fig_dyn.update_layout(showlegend=False, margin=dict(t=20, b=10))
                
                elif sel_viz == "Вертикальные столбцы (Bar)":
                    fig_dyn = px.bar(var_counts, x='Категория', y='Количество', text='Количество', color='Категория', color_discrete_sequence=px.colors.qualitative.Set2)
                    fig_dyn.update_traces(textposition='outside', textfont_size=14)
                    fig_dyn.update_layout(showlegend=False, xaxis_title="", yaxis_title="Количество чел.", margin=dict(t=20, b=10))
                    
                elif sel_viz == "Горизонтальные столбцы (Bar)":
                    fig_dyn = px.bar(var_counts, y='Категория', x='Количество', orientation='h', text='Количество', color='Категория', color_discrete_sequence=px.colors.qualitative.Set2)
                    fig_dyn.update_traces(textposition='outside', textfont_size=14)
                    fig_dyn.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'}, yaxis_title="", xaxis_title="Количество чел.", margin=dict(t=20, b=10))
                    
                elif sel_viz == "Древовидная карта (Treemap)":
                    fig_dyn = px.treemap(var_counts, path=['Категория'], values='Количество', color='Количество', color_continuous_scale='Blues')
                    fig_dyn.update_traces(textinfo="label+value+percent entry", textfont_size=14)
                    fig_dyn.update_layout(margin=dict(t=20, b=10, l=10, r=10))
                
                # Вывод графика на экран
                st.plotly_chart(fig_dyn, use_container_width=True)
            else:
                st.info("Нет доступных категориальных данных (Пол, Работа и т.д.) для построения.")

    with tab1_stats:
        st.subheader("Описательная статистика и форма распределения")
        c1_s, c2_s = st.columns([1, 1.2]) 
        
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        default_cols = [c for c in ['Age', 'IPL_Total', 'M_Sum_Zh', 'B_Altruistic'] if c in df.columns]
        
        # --- 3. ИНТЕРАКТИВНЫЙ ВИЗУАЛИЗАТОР РАСПРЕДЕЛЕНИЙ ---
        with c1_s:
            st.markdown("#### 🎻 Визуализация распределения")
            var_to_plot = st.selectbox("Выберите показатель:", numeric_cols, format_func=get_name)
            plot_type = st.radio("Тип графика:", ["Violin (Скрипичный)", "Boxplot (Ящик с усами)", "Гистограмма"], horizontal=True)
            
            if var_to_plot:
                if plot_type == "Violin (Скрипичный)":
                    fig_dist = px.violin(df, y=var_to_plot, box=True, points="all", title=get_name(var_to_plot), color_discrete_sequence=['#9b59b6'])
                elif plot_type == "Boxplot (Ящик с усами)":
                    fig_dist = px.box(df, y=var_to_plot, points="all", title=get_name(var_to_plot), color_discrete_sequence=['#e67e22'])
                else:
                    fig_dist = px.histogram(df, x=var_to_plot, marginal="box", title=get_name(var_to_plot), color_discrete_sequence=['#2ecc71'])
                
                st.plotly_chart(fig_dist, use_container_width=True)

        # Старая таблица статистики
        with c2_s:
            st.markdown("#### 📋 Подробная статистика")
            sel_stat_cols = st.multiselect("Выберите показатели для таблицы:", numeric_cols, default=default_cols, format_func=get_name)
            if sel_stat_cols:
                stats_df = get_descriptive_stats(df, sel_stat_cols)
                # Округляем значения для красоты
                formatted_df = stats_df.copy()
                for c in ['Среднее', 'SD', 'Медиана', 'Skew', 'Kurtosis']:
                    if c in formatted_df.columns:
                        formatted_df[c] = formatted_df[c].round(2)
                        
                st.dataframe(
                    formatted_df.style.background_gradient(cmap='Blues', subset=['Среднее', 'SD']),
                    use_container_width=True,
                    hide_index=True
                )
                st.caption("ℹ️ **Skew (Асимметрия)**: 0 = симметрично. **Kurtosis (Эксцесс)**: >0 = острый пик. **p > 0.05** = распределение нормальное.")

    with tab1_cross:
        st.subheader("Кросс-табуляция (пересечение признаков)")
        st.markdown("Позволяет изучить состав выборки на пересечении двух демографических параметров.")
        # --- 4. КРОСС-ТАБУЛЯЦИЯ ---
        cat_cols = [c for c in df.columns if df[c].dtype == 'object' or df[c].nunique() < 10]
        
        cross_c1, cross_c2 = st.columns(2)
        with cross_c1:
            cross_x = st.selectbox("1. Разбить столбцы по (Ось X):", cat_cols, index=0)
        with cross_c2:
            cross_y = st.selectbox("2. Заливка цветом (Группы):", cat_cols, index=1 if len(cat_cols)>1 else 0)
            
        if cross_x and cross_y:
            st.markdown("---")
            col_x1, col_x2 = st.columns(2)
            
            with col_x1:
                st.markdown("#### 📊 Структура в процентах")
                # Нормированный график (Stacked bar) по столбцам
                ct_pct = pd.crosstab(df[cross_x], df[cross_y], normalize='index') * 100
                fig_cross = px.bar(ct_pct, barmode="stack", title=f"Из чего состоит группа '{cross_x}' (%)", 
                                   labels={'value': '%', cross_x: cross_x}, color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_cross, use_container_width=True)

            with col_x2:
                st.markdown("#### 🔢 Таблица абсолютных значений")
                # Таблица сопряженности
                ct = pd.crosstab(df[cross_y], df[cross_x], margins=True, margins_name="Всего")
                st.dataframe(ct.style.background_gradient(cmap='YlGnBu', axis=None), use_container_width=True)

# === TAB 2: МЕТОДИКИ ===
with tab2:
    st.header("Анализ методик")
    
    # --- ВЫБОР РЕЖИМА И РЕСПОНДЕНТА ---
    analysis_mode = st.radio("Режим анализа:", ["Сводный (Средние по отфильтрованной группе)", "Индивидуальный (Конкретный респондент)"], horizontal=True)
    
    if analysis_mode == "Индивидуальный (Конкретный респондент)":
        respondent_list = df.apply(lambda x: f"{x.get('FIO', f'Строка {x.name}')} | Пол: {x.get('Gender', '?')} | Возраст: {x.get('Age', '?')}", axis=1)
        selected_id = st.selectbox("Выберите респондента:", respondent_list.index, format_func=lambda x: respondent_list[x])
        target_data = df.loc[[selected_id]] 
    else:
        target_data = df 
        
    subtab_b, subtab_m, subtab_i = st.tabs(["Братусь (Смыслы)", "Мильман (Мотивация)", "ИПЛ (Инновации)"])
    
    with subtab_b:
        st.subheader("Жизненные смыслы")
        b_cols = [c for c in target_data.columns if c.startswith('B_')]
        if b_cols:
            means = target_data[b_cols].mean().sort_values(ascending=True) 
            labels = [get_name(c).replace('Братусь: ', '') for c in means.index]
            visual_weight = 25 - means.values
            
            fig_b = go.Figure(go.Bar(
                x=visual_weight,
                y=labels,
                orientation='h',
                marker=dict(
                    color=means.values,
                    colorscale=[[0, '#27ae60'], [0.5, '#f1c40f'], [1, '#e74c3c']], 
                    showscale=True, 
                    colorbar=dict(title="Балл", tickvals=[5, 15, 25])
                ),
                text=np.round(means.values, 1),
                textposition='outside',
                textfont=dict(size=14),
                hovertemplate="Шкала: %{y}<br>Балл (сумма рангов): %{text}<extra></extra>"
            ))
            
            fig_b.update_layout(
                title="Жизненные смыслы (чем длиннее полоса, тем важнее смысл)",
                xaxis=dict(showticklabels=False, range=[0, 26]), 
                yaxis=dict(autorange="reversed"),
                height=650, 
                margin=dict(r=100),
                font=dict(size=14) 
            )
            st.plotly_chart(fig_b, use_container_width=True)
            st.markdown("<div style='text-align:center; font-size: 16px;'><span style='color:#27ae60'>■</span> ведущие (≤9) &nbsp;&nbsp; <span style='color:#f1c40f'>■</span> нейтральные (10-17) &nbsp;&nbsp; <span style='color:#e74c3c'>■</span> игнорируемые (≥18)</div>", unsafe_allow_html=True)
            
            # --- ТЕКСТОВЫЙ СПИСОК БРАТУСЯ ---
            st.markdown("---")
            st.markdown("#### 📋 Рейтинг жизненных смыслов")
            list_c1, list_c2 = st.columns(2)
            items = list(means.items())
            half = len(items) // 2 + (len(items) % 2) 
            
            for i, (col, val) in enumerate(items):
                scale_name = get_name(col).replace('Братусь: ', '')
                if val <= 9: 
                    color = "#27ae60"
                    status = "Доминируют"
                elif val <= 17: 
                    color = "#f1c40f"
                    status = "Представлены достаточно"
                else: 
                    color = "#e74c3c"
                    status = "Представлены слабо"
                
                item_html = f"<div style='font-size: 15px; margin-bottom: 5px;'><b>{i+1}.</b> {scale_name} — <span style='color:{color}; font-weight:bold;'>{val:.1f} ({status})</span></div>"
                if i < half:
                    list_c1.markdown(item_html, unsafe_allow_html=True)
                else:
                    list_c2.markdown(item_html, unsafe_allow_html=True)

        else:
            st.info("Колонки B_ не найдены")

    with subtab_m:
        st.subheader("Мотивационная структура (Мильман)")
        st.caption("Сравнение Идеального (чего хочу) и Реального (что имею) состояний.")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            if analysis_mode == "Индивидуальный (Конкретный респондент)":
                show_group_m = st.checkbox("📊 Сравнить со средним по группе (серый фон)", key="m_gr")
            else:
                show_group_m = False
        with col_t2:
            show_frust = st.checkbox("🔥 Показать зоны фрустрации и текстовый анализ", key="m_fr")
        
        scale_keys = ['P', 'K', 'S', 'O', 'D', 'DR', 'OD']
        scale_names = ['Жизнеобеспечение', 'Комфорт', 'Статус', 'Общение', 'Дело', 'Творчество', 'Общ. польза']
        
        if f"M_{scale_keys[0]}_Zh-id" not in target_data.columns:
            st.warning("⚠️ Колонки для методики Мильмана не найдены.")
        else:
            col_m1, col_m2 = st.columns(2)
            
            fill_arg = 'tonexty' if show_frust else 'none'
            fill_color = 'rgba(231, 76, 60, 0.2)' if show_frust else None
            
            # --- ИЗМЕНЕНИЕ: ФУНКЦИЯ ДЛЯ РАСЧЕТА ТИПА ПРОФИЛЯ ---
            def get_mot_profile_type(ideal_vals):
                sum_develop = ideal_vals[4] + ideal_vals[5] + ideal_vals[6]
                sum_maintain = ideal_vals[0] + ideal_vals[1] + ideal_vals[2]
                diff = sum_develop - sum_maintain
                
                if diff >= 5: return "Прогрессивный"
                elif diff <= -5: return "Регрессивный"
                else:
                    peaks = 0
                    for i in range(7):
                        v = ideal_vals[i]
                        if i == 0:
                            if v >= ideal_vals[1] + 4: peaks += 1
                        elif i == 6:
                            if v >= ideal_vals[5] + 4: peaks += 1
                        else:
                            if v >= ideal_vals[i-1] + 2 and v >= ideal_vals[i+1] + 2: peaks += 1
                    if peaks >= 3: return "Импульсивный"
                    elif peaks == 2: return "Экспрессивный"
                    else: return "Уплощенный"

            # Предрасчет данных для сфер
            means_zh_id = [target_data[f"M_{s}_Zh-id"].mean() for s in scale_keys]
            means_zh_re = [target_data[f"M_{s}_Zh-re"].mean() for s in scale_keys]
            mot_type_zh = get_mot_profile_type(means_zh_id)
            
            means_rb_id = [target_data[f"M_{s}_Rb-id"].mean() for s in scale_keys]
            means_rb_re = [target_data[f"M_{s}_Rb-re"].mean() for s in scale_keys]
            mot_type_rb = get_mot_profile_type(means_rb_id)
            
            with col_m1:
                st.markdown("#### 🏠 Общежитейская сфера")
                st.info(f"🧠 **Тип профиля:** {mot_type_zh}") # Вывод типа профиля
                
                fig_zh = go.Figure()
                if show_group_m:
                    grp_zh_re = [df[f"M_{s}_Zh-re"].mean() for s in scale_keys]
                    fig_zh.add_trace(go.Scatter(x=scale_names, y=grp_zh_re, mode='lines', name='Группа (Реал)', line=dict(color='rgba(180,180,180,0.6)', width=5)))
                    
                fig_zh.add_trace(go.Scatter(x=scale_names, y=means_zh_id, mode='lines+markers', name='Желаемое', line=dict(color='blue', dash='dash', width=3), marker=dict(size=8)))
                fig_zh.add_trace(go.Scatter(x=scale_names, y=means_zh_re, mode='lines+markers', name='Реальное', fill=fill_arg, fillcolor=fill_color, line=dict(color='red', width=3), marker=dict(size=8)))
                
                max_zh = max(max(means_zh_id), max(means_zh_re))
                fig_zh.update_layout(yaxis=dict(range=[0, max_zh + 2]), height=400, margin=dict(l=20, r=20, t=10, b=20), font=dict(size=14))
                st.plotly_chart(fig_zh, use_container_width=True)
                
            with col_m2:
                st.markdown("#### 💼 Учебная/Рабочая сфера")
                st.info(f"🧠 **Тип профиля:** {mot_type_rb}") # Вывод типа профиля
                
                fig_rb = go.Figure()
                if show_group_m:
                    grp_rb_re = [df[f"M_{s}_Rb-re"].mean() for s in scale_keys]
                    fig_rb.add_trace(go.Scatter(x=scale_names, y=grp_rb_re, mode='lines', name='Группа (Реал)', line=dict(color='rgba(180,180,180,0.6)', width=5)))
                
                fig_rb.add_trace(go.Scatter(x=scale_names, y=means_rb_id, mode='lines+markers', name='Желаемое', line=dict(color='green', dash='dash', width=3), marker=dict(size=8)))
                fig_rb.add_trace(go.Scatter(x=scale_names, y=means_rb_re, mode='lines+markers', name='Реальное', fill=fill_arg, fillcolor=fill_color, line=dict(color='orange', width=3), marker=dict(size=8)))
                
                max_rb = max(max(means_rb_id), max(means_rb_re))
                fig_rb.update_layout(yaxis=dict(range=[0, max_rb + 2]), height=400, margin=dict(l=20, r=20, t=10, b=20), font=dict(size=14))
                st.plotly_chart(fig_rb, use_container_width=True)
            
            if show_frust:
                st.markdown("---")
                st.markdown("#### 📝 Анализ фрустрации (неудовлетворенности)")
                
                def print_frustration_analysis(id_vals, re_vals, sphere_name):
                    deltas = [i - r for i, r in zip(id_vals, re_vals)]
                    max_delta_idx = np.argmax(deltas)
                    max_delta_val = deltas[max_delta_idx]
                    
                    frust_items = []
                    for idx, d in enumerate(deltas):
                        if d > 0:
                            frust_items.append(f"*{scale_names[idx]}* (дельта: **{d:.1f}**)")
                    
                    if max_delta_val > 0:
                        st.markdown(f"**{sphere_name}:**")
                        st.error(f"⚠️ Наибольшая фрустрация выявлена в шкале: **«{scale_names[max_delta_idx]}»** (неудовлетворенность: **{max_delta_val:.1f}** балла).")
                        if len(frust_items) > 1:
                            st.markdown(f"Также зафиксирована разница в шкалах: {', '.join(frust_items)}.")
                    else:
                        st.success(f"**{sphere_name}:** Значимых зон фрустрации не выявлено (Реальное состояние полностью покрывает Желаемое).")

                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    print_frustration_analysis(means_zh_id, means_zh_re, "Общежитейская сфера")
                with col_f2:
                    print_frustration_analysis(means_rb_id, means_rb_re, "Учебная/Рабочая сфера")
            
            # --- ЭМОЦИОНАЛЬНЫЙ ПРОФИЛЬ ---
            emo_cols = ['M_Est', 'M_East', 'M_Fst', 'M_Fast']
            if all(col in target_data.columns for col in emo_cols):
                st.markdown("---")
                st.markdown("<h4 style='text-align: center;'>🎭 Эмоциональный профиль</h4>", unsafe_allow_html=True)
                emo_means = target_data[emo_cols].mean()
                
                e_st, e_ast = emo_means['M_Est'], emo_means['M_East']
                f_st, f_ast = emo_means['M_Fst'], emo_means['M_Fast']
                
                if e_st > e_ast and f_st > f_ast: emo_type = "Стенический"
                elif e_ast > e_st and f_ast > f_st: emo_type = "Астенический"
                elif e_ast > e_st and f_st > f_ast: emo_type = "Смешанный стенический"
                elif e_st > e_ast and f_ast > f_st: emo_type = "Смешанный астенический"
                else: emo_type = "Не определён (баланс показателей)"
                
                st.markdown(f"<div style='text-align:center; margin-bottom: 10px; font-size: 16px; color: #34495e;'><b>Тип эмоционального профиля:</b> {emo_type}</div>", unsafe_allow_html=True)
                
                col_e1, col_e2, col_e3 = st.columns([1, 1.2, 1])
                with col_e2:
                    fig_emo = go.Figure()
                    
                    if show_group_m:
                        grp_emo = df[emo_cols].mean()
                        fig_emo.add_trace(go.Scatter(x=["Обычное состояние", "Стресс"], y=[grp_emo['M_Est'], grp_emo['M_Fst']], mode='lines', name='Группа (Стен.)', line=dict(color='rgba(180,180,180,0.6)', width=4)))
                        fig_emo.add_trace(go.Scatter(x=["Обычное состояние", "Стресс"], y=[grp_emo['M_East'], grp_emo['M_Fast']], mode='lines', name='Группа (Астен.)', line=dict(color='rgba(180,180,180,0.6)', width=4, dash='dot')))
                    
                    fig_emo.add_trace(go.Scatter(
                        x=["Обычное состояние", "Стресс"], y=[emo_means['M_Est'], emo_means['M_Fst']], mode='lines+markers', name='Стенические', line=dict(color='#27ae60', width=5), marker=dict(size=12)
                    ))
                    fig_emo.add_trace(go.Scatter(
                        x=["Обычное состояние", "Стресс"], y=[emo_means['M_East'], emo_means['M_Fast']], mode='lines+markers', name='Астенические', line=dict(color='#e74c3c', width=4, dash='dot'), marker=dict(size=10, symbol='diamond')
                    ))
                    
                    max_emo = emo_means.max()
                    fig_emo.update_layout(
                        yaxis=dict(range=[0, max_emo + 4]), height=480, margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5), font=dict(size=14) 
                    )
                    st.plotly_chart(fig_emo, use_container_width=True)

    with subtab_i:
        st.subheader("Инновационный потенциал личности (ИПЛ)")
        
        if analysis_mode == "Индивидуальный (Конкретный респондент)":
            show_group_i = st.checkbox("📊 Сравнить со средними показателями группы", key="i_gr")
        else:
            show_group_i = False
            
        if 'IPL_Total' in target_data.columns:
            total_mean = target_data['IPL_Total'].mean()
            if total_mean >= 118: ipl_level, ipl_color = "Высокий", "linear-gradient(90deg, #2ecc71, #27ae60)"
            elif total_mean >= 95: ipl_level, ipl_color = "Средний", "linear-gradient(90deg, #3498db, #2980b9)"
            else: ipl_level, ipl_color = "Низкий", "linear-gradient(90deg, #e74c3c, #c0392b)"
                
            ipl_percent = min(100, max(0, (total_mean / 180) * 100))
            
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:5px;">
                    <div style="font-size:2.5em; font-weight:bold; color:#2c3e50;">{total_mean:.1f}</div>
                    <div style="font-size:1.3em; font-weight:bold; color:#555;">Уровень: {ipl_level}</div>
                </div>
                <div style="background:#eee; border-radius:20px; height:25px; overflow:hidden; margin-bottom:5px; width: 100%;">
                    <div style="height:100%; width:{ipl_percent}%; background:{ipl_color}; border-radius: 20px;"></div>
                </div>
                <div style="font-size:1em; color: gray; margin-bottom:10px;">Максимум 180 баллов. Нормы: < 95 (Низкий) | 95-117 (Средний) | ≥ 118 (Высокий)</div>
            """, unsafe_allow_html=True)
            
            if show_group_i:
                grp_total = df['IPL_Total'].mean()
                st.markdown(f"<div style='color:gray; font-weight:bold; margin-bottom:20px;'>Справочно: Средний ИПЛ по группе = {grp_total:.1f}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 1])
            with c1:
                comp_cols = ['IPL_G', 'IPL_A', 'IPL_P']
                available_comp = [c for c in comp_cols if c in target_data.columns]
                if available_comp:
                    comp_means = target_data[available_comp].mean()
                    fig_comp = go.Figure()
                    
                    fig_comp.add_trace(go.Bar(name='Респондент', x=comp_means.index, y=comp_means.values, text=[f"{v:.1f}" for v in comp_means.values], textposition='outside', marker_color='#3498db'))
                    
                    if show_group_i:
                        grp_means = df[available_comp].mean()
                        fig_comp.add_trace(go.Bar(name='Группа', x=grp_means.index, y=grp_means.values, text=[f"{v:.1f}" for v in grp_means.values], textposition='outside', marker_color='lightgrey'))

                    fig_comp.update_layout(barmode='group', title="Структура ИПЛ (Г-А-П)", showlegend=show_group_i, yaxis=dict(range=[0, comp_means.max() * 1.3]), font=dict(size=14))
                    st.plotly_chart(fig_comp, use_container_width=True)

            with c2:
                level_cols = ['IPL_Level_Nature', 'IPL_Level_Social', 'IPL_Level_Culture', 'IPL_Level_Life']
                available_levels = [c for c in level_cols if c in target_data.columns]
                if available_levels:
                    l_means = target_data[available_levels].mean()
                    clean_index = [x.replace('IPL_Level_', '') for x in l_means.index]
                    
                    fig_lvl = go.Figure()
                    fig_lvl.add_trace(go.Bar(name='Респондент', y=clean_index, x=l_means.values, orientation='h', text=[f"{v:.1f}" for v in l_means.values], textposition='outside', marker_color='#2ecc71'))
                    
                    if show_group_i:
                        grp_l_means = df[available_levels].mean()
                        fig_lvl.add_trace(go.Bar(name='Группа', y=clean_index, x=grp_l_means.values, orientation='h', text=[f"{v:.1f}" for v in grp_l_means.values], textposition='outside', marker_color='lightgrey'))

                    fig_lvl.update_layout(barmode='group', title="Средние баллы по уровням", showlegend=show_group_i, xaxis=dict(range=[0, l_means.max() * 1.3]), font=dict(size=14))
                    st.plotly_chart(fig_lvl, use_container_width=True)

            st.markdown("---")
            st.subheader("Типы реализации возможностей")
            type_pairs = [
                ('IPL_Type_OI', 'IPL_Type_FN', 'Поиск информации'),
                ('IPL_Type_PD', 'IPL_Type_NG', 'Оценка нового'),
                ('IPL_Type_IP', 'IPL_Type_VP', 'Действие')
            ]
            cols_types = st.columns(3)
            for i, (k1, k2, title) in enumerate(type_pairs):
                if k1 in target_data.columns and k2 in target_data.columns:
                    with cols_types[i]:
                        m1, m2 = target_data[k1].mean(), target_data[k2].mean()
                        fig_t = go.Figure()
                        
                        fig_t.add_trace(go.Bar(name=k1.replace('IPL_Type_', ''), x=[k1.replace('IPL_Type_', '')], y=[m1], text=[f"{m1:.1f}"], textposition='auto', marker_color='#9b59b6'))
                        fig_t.add_trace(go.Bar(name=k2.replace('IPL_Type_', ''), x=[k2.replace('IPL_Type_', '')], y=[m2], text=[f"{m2:.1f}"], textposition='auto', marker_color='#34495e'))
                        
                        if show_group_i:
                            gm1, gm2 = df[k1].mean(), df[k2].mean()
                            fig_t.add_trace(go.Bar(name='Группа', x=[k1.replace('IPL_Type_', '')], y=[gm1], text=[f"{gm1:.1f}"], textposition='auto', marker_color='lightgrey', showlegend=False))
                            fig_t.add_trace(go.Bar(name='Группа', x=[k2.replace('IPL_Type_', '')], y=[gm2], text=[f"{gm2:.1f}"], textposition='auto', marker_color='lightgrey', showlegend=False))

                        fig_t.update_layout(barmode='group', title=title, showlegend=show_group_i, height=300, margin=dict(l=10, r=10, t=40, b=10), font=dict(size=14), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
                        st.plotly_chart(fig_t, use_container_width=True)
        else:
            st.warning("Колонки ИПЛ не найдены.")


# === TAB 3: СРАВНЕНИЕ ГРУПП И ПРОВЕРКА ГИПОТЕЗ ===
with tab3:
    st.header("🆚 Сравнение групп и проверка гипотез")
    
    # Внутреннее разделение на 3 инструмента
    subtab_single, subtab_mass, subtab_auto = st.tabs([
        "🎯 Детальный анализ одной шкалы", 
        "📊 Сравнение профилей методик", 
        "💡 Авто-поиск всех различий"
    ])
    
    # Собираем категориальные колонки для выбора групп
    cat_cols = [c for c in df.columns if df[c].dtype == 'object' or df[c].nunique() < 10]
    
    # ---------------------------------------------------------
    # 1. ОДИНОЧНЫЙ ТЕСТ (Базовый)
    # ---------------------------------------------------------
    with subtab_single:
        st.subheader("Проверка гипотез (T-test / ANOVA) для конкретного показателя")
        
        col_set1, col_set2 = st.columns(2)
        with col_set1:
            group_var_single = st.selectbox("1. Разделить группы по:", cat_cols, key="grp_single")
        with col_set2:
            num_cols = df.select_dtypes(include=np.number).columns.tolist()
            target_var_single = st.selectbox("2. Сравнить показатель:", num_cols, key="tgt_single", format_func=get_name)

        if group_var_single and target_var_single:
            fig_box = px.box(df, x=group_var_single, y=target_var_single, color=group_var_single, 
                             points="all", title=f"{get_name(target_var_single)} по группам {group_var_single}")
            st.plotly_chart(fig_box, use_container_width=True)

            st.markdown("#### Результаты статистического теста")
            res_df, p_val_res = smart_compare_groups(df, group_var_single, target_var_single)
            
            if res_df is not None:
                st.table(res_df)
                if p_val_res < 0.05:
                    st.success("✅ Обнаружены **статистически значимые различия** (p < 0.05).")
                else:
                    st.warning("❌ Значимых различий не обнаружено (p > 0.05).")
            else:
                st.error("Не удалось провести тест (недостаточно данных).")

    # ---------------------------------------------------------
    # 2. МАССОВОЕ СРАВНЕНИЕ ПРОФИЛЕЙ
    # ---------------------------------------------------------
    with subtab_mass:
        st.subheader("Визуальное сравнение групп по всем шкалам")
        group_var_mass = st.selectbox("Выберите признак для группировки профилей:", cat_cols, key="grp_mass")
        
        if group_var_mass and len(df[group_var_mass].dropna().unique()) >= 2:
            
            # --- БРАТУСЬ ---
            st.markdown("### 1. Жизненные смыслы (Братусь)")
            b_cols = [c for c in df.columns if c.startswith('B_')]
            if b_cols:
                b_res = df.groupby(group_var_mass)[b_cols].mean().reset_index().melt(id_vars=group_var_mass)
                b_res['variable'] = b_res['variable'].apply(lambda x: get_name(x).replace('Братусь: ', ''))
                fig_b = px.bar(b_res, x='variable', y='value', color=group_var_mass, barmode='group', 
                               title="Средние ранги (Меньше = Важнее)")
                fig_b.update_layout(xaxis_title="", yaxis_title="Ранг")
                st.plotly_chart(fig_b, use_container_width=True)
            
            # --- МИЛЬМАН ---
            st.markdown("### 2. Мотивационная структура (Мильман)")
            m_scales = ['P', 'K', 'S', 'O', 'D', 'DR', 'OD']
            
            tab_m_life, tab_m_work, tab_m_emo = st.tabs(["🏠 Жизнь", "💼 Работа", "🎭 Эмоции"])
            
            with tab_m_life:
                col_ml1, col_ml2 = st.columns(2)
                with col_ml1:
                    m_re_zh = [f"M_{s}_Zh-re" for s in m_scales]
                    if all(c in df.columns for c in m_re_zh):
                        res_zh_re = df.groupby(group_var_mass)[m_re_zh].mean().reset_index().melt(id_vars=group_var_mass)
                        res_zh_re['variable'] = res_zh_re['variable'].apply(lambda x: x.split('_')[1].split('-')[0])
                        fig_m_z_re = px.line(res_zh_re, x='variable', y='value', color=group_var_mass, markers=True, title="Реальное состояние")
                        st.plotly_chart(fig_m_z_re, use_container_width=True)
                with col_ml2:
                    m_id_zh = [f"M_{s}_Zh-id" for s in m_scales]
                    if all(c in df.columns for c in m_id_zh):
                        res_zh_id = df.groupby(group_var_mass)[m_id_zh].mean().reset_index().melt(id_vars=group_var_mass)
                        res_zh_id['variable'] = res_zh_id['variable'].apply(lambda x: x.split('_')[1].split('-')[0])
                        fig_m_z_id = px.line(res_zh_id, x='variable', y='value', color=group_var_mass, markers=True, line_dash=group_var_mass, title="Идеальное состояние")
                        st.plotly_chart(fig_m_z_id, use_container_width=True)

            with tab_m_work:
                col_mw1, col_mw2 = st.columns(2)
                with col_mw1:
                    m_re_rb = [f"M_{s}_Rb-re" for s in m_scales]
                    if all(c in df.columns for c in m_re_rb):
                        res_rb_re = df.groupby(group_var_mass)[m_re_rb].mean().reset_index().melt(id_vars=group_var_mass)
                        res_rb_re['variable'] = res_rb_re['variable'].apply(lambda x: x.split('_')[1].split('-')[0])
                        fig_m_r_re = px.line(res_rb_re, x='variable', y='value', color=group_var_mass, markers=True, title="Реальное состояние")
                        st.plotly_chart(fig_m_r_re, use_container_width=True)
                with col_mw2:
                    m_id_rb = [f"M_{s}_Rb-id" for s in m_scales]
                    if all(c in df.columns for c in m_id_rb):
                        res_rb_id = df.groupby(group_var_mass)[m_id_rb].mean().reset_index().melt(id_vars=group_var_mass)
                        res_rb_id['variable'] = res_rb_id['variable'].apply(lambda x: x.split('_')[1].split('-')[0])
                        fig_m_r_id = px.line(res_rb_id, x='variable', y='value', color=group_var_mass, markers=True, line_dash=group_var_mass, title="Идеальное состояние")
                        st.plotly_chart(fig_m_r_id, use_container_width=True)
                        
            with tab_m_emo:
                emo_cols = ['M_Est', 'M_East', 'M_Fst', 'M_Fast']
                if all(c in df.columns for c in emo_cols):
                    emo_res = df.groupby(group_var_mass)[emo_cols].mean().reset_index().melt(id_vars=group_var_mass)
                    emo_res['variable'] = emo_res['variable'].apply(lambda x: get_name(x).replace('Мильман: ', ''))
                    fig_emo = px.bar(emo_res, x='variable', y='value', color=group_var_mass, barmode='group', title="Эмоциональный профиль")
                    fig_emo.update_layout(xaxis_title="")
                    st.plotly_chart(fig_emo, use_container_width=True)

            # --- ИПЛ ---
            st.markdown("### 3. Инновационный потенциал (ИПЛ)")
            
            c_ipl1, c_ipl2 = st.columns(2)
            with c_ipl1:
                # Аспекты (Радар)
                i_cols = ['IPL_G', 'IPL_A', 'IPL_P']
                if all(c in df.columns for c in i_cols):
                    ipl_means = df.groupby(group_var_mass)[i_cols].mean().reset_index()
                    fig_i_radar = go.Figure()
                    for i, row in ipl_means.iterrows():
                        fig_i_radar.add_trace(go.Scatterpolar(
                            r=row[i_cols].values,
                            theta=['Гносеологический', 'Аксиологический', 'Праксеологический'],
                            fill='toself',
                            name=str(row[group_var_mass])
                        ))
                    fig_i_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), title="Аспекты Г-А-П", margin=dict(t=40, b=20))
                    st.plotly_chart(fig_i_radar, use_container_width=True)
            
            with c_ipl2:
                # Общий балл
                if 'IPL_Total' in df.columns:
                    fig_i_tot = px.box(df, x=group_var_mass, y='IPL_Total', color=group_var_mass, title="Общий уровень ИПЛ")
                    st.plotly_chart(fig_i_tot, use_container_width=True)

            c_ipl3, c_ipl4 = st.columns(2)
            with c_ipl3:
                # Типы реализации
                types_cols = ['IPL_Type_OI', 'IPL_Type_FN', 'IPL_Type_PD', 'IPL_Type_NG', 'IPL_Type_IP', 'IPL_Type_VP']
                avail_types = [c for c in types_cols if c in df.columns]
                if avail_types:
                    res_types = df.groupby(group_var_mass)[avail_types].mean().reset_index().melt(id_vars=group_var_mass)
                    res_types['variable'] = res_types['variable'].apply(lambda x: x.split('_')[-1]) # Только буквы ОИ, ФН и тд
                    fig_types = px.bar(res_types, x='variable', y='value', color=group_var_mass, barmode='group', title="Типы реализации")
                    st.plotly_chart(fig_types, use_container_width=True)
                    
            with c_ipl4:
                # Уровни
                lvl_cols = ['IPL_Level_Nature', 'IPL_Level_Social', 'IPL_Level_Culture', 'IPL_Level_Life']
                avail_lvls = [c for c in lvl_cols if c in df.columns]
                if avail_lvls:
                    res_lvl = df.groupby(group_var_mass)[avail_lvls].mean().reset_index().melt(id_vars=group_var_mass)
                    res_lvl['variable'] = res_lvl['variable'].apply(lambda x: get_name(x).replace('ИПЛ: ', ''))
                    fig_lvl = px.bar(res_lvl, x='value', y='variable', color=group_var_mass, orientation='h', barmode='group', title="Уровни взаимодействия")
                    st.plotly_chart(fig_lvl, use_container_width=True)

    # ---------------------------------------------------------
    # 3. АВТО-ПОИСК РАЗЛИЧИЙ (Супер-функция)
    # ---------------------------------------------------------
    with subtab_auto:
        st.subheader("Автоматический сканер значимых различий")
        st.markdown("Выберите группирующую переменную, и алгоритм проверит все шкалы на наличие статистически значимых различий.")
        
        group_var_auto = st.selectbox("Признак для анализа:", cat_cols, key="grp_auto")
        
        if st.button("🚀 Начать сканирование"):
            with st.spinner("Считаем статистику..."):
                auto_results = []
                num_cols = df.select_dtypes(include=np.number).columns.tolist()
                
                for col in num_cols:
                    clean_df = df[[group_var_auto, col]].dropna()
                    groups = clean_df[group_var_auto].unique()
                    
                    if len(groups) < 2: continue
                    
                    try:
                        # Проверка нормальности для сканера
                        is_normal = True
                        for g in groups:
                            g_data = clean_df[clean_df[group_var_auto] == g][col]
                            if len(g_data) >= 3 and pg.normality(g_data)['pval'].values[0] < 0.05:
                                is_normal = False
                                break

                        if len(groups) == 2:
                            g1 = clean_df[clean_df[group_var_auto] == groups[0]][col]
                            g2 = clean_df[clean_df[group_var_auto] == groups[1]][col]
                            
                            if is_normal:
                                res = pg.ttest(g1, g2, correction=True)
                                p_val, eff, eff_name = res['p-val'].values[0], res['cohen-d'].values[0], "Cohen's d"
                                test_used = "T-test" # <--- Добавили название теста
                            else:
                                res = pg.mwu(g1, g2)
                                p_val, eff, eff_name = res['p-val'].values[0], res['RBC'].values[0], "Rank-Biserial"
                                test_used = "Mann-Whitney" # <--- Добавили название теста
                        else:
                            if is_normal:
                                res = pg.anova(data=clean_df, dv=col, between=group_var_auto)
                                p_val, eff, eff_name = res['p-unc'].values[0], res['np2'].values[0], "Eta-sq"
                                test_used = "ANOVA" # <--- Добавили название теста
                            else:
                                res = pg.kruskal(data=clean_df, dv=col, between=group_var_auto)
                                p_val, eff, eff_name = res['p-unc'].values[0], res['H'].values[0], "H-stat"
                                test_used = "Kruskal-Wallis" # <--- Добавили название теста
                            
                        if p_val < 0.05:
                            means = clean_df.groupby(group_var_auto)[col].mean()
                            max_group = means.idxmax()
                            stars = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else "*")
                            
                            auto_results.append({
                                "Показатель": get_name(col),
                                "Тест": test_used, # <--- ВЫВЕЛИ В ИТОГОВУЮ ТАБЛИЦУ
                                "p-value": f"{p_val:.4f} {stars}",
                                "Метрика эффекта": eff_name,
                                "Размер эффекта": round(eff, 3),
                                "Выше у группы": max_group
                            })
                    except:
                        pass
                
                if not auto_results:
                    st.info(f"Значимых различий (p < 0.05) между группами '{group_var_auto}' не найдено.")
                else:
                    res_df = pd.DataFrame(auto_results).sort_values(by="Размер эффекта", ascending=False).reset_index(drop=True)
                    st.success(f"**Найдено значимых различий: {len(res_df)}** (Отсортировано по силе эффекта)")
                    
                    # Красивый вывод таблицы
                    st.dataframe(
                        res_df.style.background_gradient(cmap='Blues', subset=['Размер эффекта']),
                        use_container_width=True
                    )
                    
                    st.caption("ℹ️ **Cohen's d** (для 2 групп): 0.2 - слабый, 0.5 - средний, >0.8 - сильный эффект. **Eta-sq** (для >2 групп): 0.01 - слабый, 0.06 - средний, >0.14 - сильный.")
# === TAB 4: КОРРЕЛЯЦИИ (Step 3 part 1) ===
with tab4:
    st.header("🔗 Корреляционный анализ (в стиле SPSS)")
    
    # Логика кнопок для быстрого выбора шкал (Session State)
    if 'corr_sel' not in st.session_state:
        st.session_state.corr_sel = num_cols[:8] if len(num_cols) > 8 else num_cols

    def add_prefix(prefix):
        current = st.session_state.corr_sel
        new_items = [c for c in num_cols if c.startswith(prefix) and c not in current]
        st.session_state.corr_sel = current + new_items
    
    def clear_all():
        st.session_state.corr_sel = []

    # Кнопки быстрого добавления
    st.write("**Быстрое добавление шкал:**")
    btn_c1, btn_c2, btn_c3, btn_c4 = st.columns(4)
    btn_c1.button("➕ Добавить Братуся", on_click=add_prefix, args=('B_',))
    btn_c2.button("➕ Добавить Мильмана", on_click=add_prefix, args=('M_',))
    btn_c3.button("➕ Добавить ИПЛ", on_click=add_prefix, args=('IPL_',))
    btn_c4.button("❌ Очистить всё", on_click=clear_all)
    
    # Само поле выбора (привязано к session_state через key)
    corr_cols = st.multiselect(
        "Выберите показатели:", 
        num_cols, 
        key="corr_sel",
        format_func=get_name # Это переведет названия прямо в выпадающем списке!
    )
    
    col1, col2 = st.columns(2)
    with col1:
        method = st.radio(
    "Метод корреляции:", 
    ["spearman", "pearson"], # Поменяли местами, Спирмен теперь первый
    horizontal=True, 
    help="Spearman (ранговая) лучше подходит для психологических опросников. Pearson — для строго нормально распределенных метрических данных."
)
    with col2:
        show_stars = st.checkbox("Показывать значимость (звездочки)", value=True)
    
    if len(corr_cols) > 1:
        # --- БЛОК 1: РАСЧЕТ МАТРИЦЫ И P-VALUE ---
        df_corr = df[corr_cols].dropna()
        r_matrix = df_corr.corr(method=method)
        p_matrix = pd.DataFrame(np.ones((len(corr_cols), len(corr_cols))), columns=corr_cols, index=corr_cols)
        
        for i in range(len(corr_cols)):
            for j in range(i + 1, len(corr_cols)):
                col_i, col_j = corr_cols[i], corr_cols[j]
                res = pg.corr(df_corr[col_i], df_corr[col_j], method=method)
                p_val = res['p-val'].values[0]
                p_matrix.loc[col_i, col_j] = p_val
                p_matrix.loc[col_j, col_i] = p_val 
        
        annot_matrix = np.empty_like(r_matrix, dtype=object)
        hover_matrix = np.empty_like(r_matrix, dtype=object)
        
        for i in range(len(corr_cols)):
            for j in range(len(corr_cols)):
                r_val = r_matrix.iloc[i, j]
                p_val = p_matrix.iloc[i, j]
                
                stars = ""
                if i != j: 
                    if p_val < 0.001: stars = "***"
                    elif p_val < 0.01: stars = "**"
                    elif p_val < 0.05: stars = "*"
                
                annot_matrix[i, j] = f"{r_val:.2f}{stars}" if show_stars else f"{r_val:.2f}"
                
                # Текст для всплывающей подсказки (с полными названиями)
                hover_matrix[i, j] = (
                    f"<b>X:</b> {get_name(corr_cols[j])}<br>"
                    f"<b>Y:</b> {get_name(corr_cols[i])}<br>"
                    f"<b>r =</b> {r_val:.3f} {stars}<br>"
                    f"<b>p-value =</b> {p_val:.4f}"
                )
        
        # --- БЛОК 2: ИНТЕРАКТИВНАЯ ВИЗУАЛИЗАЦИЯ PLOTLY ---
        # Переводим названия осей для матрицы
        translated_cols = [get_name(c) for c in corr_cols]
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=r_matrix.values,
            x=translated_cols,
            y=translated_cols,
            text=annot_matrix,               
            texttemplate="%{text}",          
            customdata=hover_matrix,         
            hovertemplate="%{customdata}<extra></extra>", 
            colorscale='RdBu_r',
            zmin=-1, zmax=1
        ))
        
        plot_height = max(600, len(corr_cols) * 35) # Адаптивная высота матрицы
        
        fig_corr.update_layout(
            title=f"Матрица корреляций ({method.capitalize()})",
            height=plot_height,
            xaxis_tickangle=-45 
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        st.caption("**Как читать:** Красный = прямая связь, Синий = обратная. Значимость: * p < 0.05, ** p < 0.01, *** p < 0.001.")
        
        # --- БЛОК 3: ИНТЕРАКТИВНЫЙ ПОИСК СВЯЗЕЙ ---
        st.markdown("---")
        st.subheader("🔍 Автоматический поиск связей")
        
        filter_c1, filter_c2, filter_c3 = st.columns(3)
        with filter_c1:
            strength_preset = st.selectbox(
                "Сила связи (|r|):",
                ["Все значимые", "Слабая (0.1 - 0.3)", "Умеренная (0.3 - 0.5)", "Сильная (0.5 - 0.7)", "Очень сильная (> 0.7)", "Своё значение..."]
            )
            if strength_preset == "Своё значение...":
                custom_r = st.number_input("Минимальный модуль |r|:", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
                min_r, max_r = custom_r, 1.0
            elif strength_preset == "Слабая (0.1 - 0.3)": min_r, max_r = 0.1, 0.3
            elif strength_preset == "Умеренная (0.3 - 0.5)": min_r, max_r = 0.3, 0.5
            elif strength_preset == "Сильная (0.5 - 0.7)": min_r, max_r = 0.5, 0.7
            elif strength_preset == "Очень сильная (> 0.7)": min_r, max_r = 0.7, 1.0
            else: min_r, max_r = 0.0, 1.0

        with filter_c2:
            sig_level = st.selectbox(
                "Уровень значимости (p):",
                ["p < 0.05 (*)", "p < 0.01 (**)", "p < 0.001 (***)", "Показывать незначимые (p > 0.05)"]
            )
            if sig_level == "p < 0.05 (*)": p_thresh = 0.05
            elif sig_level == "p < 0.01 (**)": p_thresh = 0.01
            elif sig_level == "p < 0.001 (***)": p_thresh = 0.001
            else: p_thresh = 1.0 
            
        with filter_c3:
            link_type = st.radio("Направление связи:", ["Все", "Прямая (r > 0)", "Обратная (r < 0)"])

        links = []
        for i in range(len(corr_cols)):
            for j in range(i + 1, len(corr_cols)):
                c1, c2 = corr_cols[i], corr_cols[j]
                r = r_matrix.loc[c1, c2]
                p = p_matrix.loc[c1, c2]
                
                if abs(r) >= min_r and abs(r) <= max_r: 
                    if (sig_level != "Показывать незначимые (p > 0.05)" and p < p_thresh) or \
                       (sig_level == "Показывать незначимые (p > 0.05)" and p >= 0.05): 
                        if link_type == "Все" or (link_type == "Прямая (r > 0)" and r > 0) or (link_type == "Обратная (r < 0)" and r < 0): 
                            s = ""
                            if p < 0.001: s = "***"
                            elif p < 0.01: s = "**"
                            elif p < 0.05: s = "*"
                            
                            links.append({
                                'Показатель 1': get_name(c1),  # Сразу переводим
                                'Показатель 2': get_name(c2),  # Сразу переводим
                                'r': r,
                                'p-value': p,
                                'Значимость': s
                            })
                            
        if not links:
            st.info("По заданным фильтрам связей не найдено.")
        else:
            links_df = pd.DataFrame(links).sort_values(by='r', key=abs, ascending=False).reset_index(drop=True)
            
            # --- НОВЫЙ КОД: КНОПКА СКАЧИВАНИЯ СВЯЗЕЙ (EXCEL) ---
            col_l1, col_l2 = st.columns([1, 1])
            with col_l1:
                st.write(f"**Найдено связей: {len(links_df)}**")
            with col_l2:
                buffer_links = io.BytesIO()
                links_df.to_excel(buffer_links, index=False, engine='openpyxl')
                st.download_button(
                    label="📥 Скачать таблицу связей (Excel)",
                    data=buffer_links.getvalue(),
                    file_name='correlation_links.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            st.markdown("---")
            # --- КОНЕЦ НОВОГО КОДА ---
            
            for _, row in links_df.iterrows():
                color_dot = "🔴" if row['r'] > 0 else "🔵"
                st.markdown(
                    f"{color_dot} **{row['Показатель 1']}** ↔ **{row['Показатель 2']}** "
                    f"| `r = {row['r']:.2f}` {row['Значимость']} "
                    f"*(p={row['p-value']:.3f})*"
                )

# === TAB 5: КЛАСТЕРНЫЙ АНАЛИЗ (Step 3 part 2) ===
with tab5:
    st.header("🔬 Кластерный анализ (Иерархический и K-Means)")
    st.markdown("Методы классификации наблюдений (респондентов) и переменных (шкал).")

    # --- ЛОГИКА КНОПОК БЫСТРОГО ВЫБОРА ---
    # Инициализация состояния для двух разных полей (HC и KM)
    if 'hc_sel' not in st.session_state:
        st.session_state.hc_sel = num_cols[:6] if len(num_cols)>6 else num_cols
    if 'km_sel' not in st.session_state:
        st.session_state.km_sel = num_cols[:4] if len(num_cols)>4 else num_cols

    # Универсальная функция добавления префикса
    def add_to_state(state_key, prefix):
        current = st.session_state[state_key]
        new_items = [c for c in num_cols if c.startswith(prefix) and c not in current]
        st.session_state[state_key] = current + new_items
    
    # Универсальная функция очистки
    def clear_state(state_key):
        st.session_state[state_key] = []
    # ------------------------------------

    # Создаем под-вкладки для разделения методов
    subtab_hc, subtab_km = st.tabs(["🌳 Иерархическая кластеризация (SPSS)", "🎯 K-Means (Авто-выбор)"])

    # ---------------------------------------------------------
    # ПОД-ВКЛАДКА 1: ИЕРАРХИЧЕСКАЯ КЛАСТЕРИЗАЦИЯ
    # ---------------------------------------------------------
    with subtab_hc:
        st.subheader("Иерархический кластерный анализ и Дендрограммы")
        st.markdown("Позволяет визуально оценить естественные группировки (деревья) в данных.")

        # Кнопки быстрого выбора для HC
        st.write("**Быстрое добавление шкал:**")
        hc_b1, hc_b2, hc_b3, hc_b4 = st.columns(4)
        hc_b1.button("➕ Братусь", on_click=add_to_state, args=('hc_sel', 'B_'), key="hc_btn_b")
        hc_b2.button("➕ Мильман", on_click=add_to_state, args=('hc_sel', 'M_'), key="hc_btn_m")
        hc_b3.button("➕ ИПЛ", on_click=add_to_state, args=('hc_sel', 'IPL_'), key="hc_btn_i")
        hc_b4.button("❌ Очистить", on_click=clear_state, args=('hc_sel',), key="hc_btn_clear")

        hc_col1, hc_col2 = st.columns(2)
        with hc_col1:
            hc_features = st.multiselect(
                "Выберите шкалы для кластеризации:",
                num_cols,
                key="hc_sel",
                format_func=get_name
            )
        with hc_col2:
            possible_labels = ["Номер строки (Index)"] + [c for c in df.columns if df[c].dtype == 'object']
            obs_label = st.selectbox("Подписывать респондентов по:", possible_labels)

        if len(hc_features) >= 2:
            # Подготовка данных
            df_hc = df.dropna(subset=hc_features).copy()
            X_hc = df_hc[hc_features]

            from sklearn.preprocessing import StandardScaler
            X_scaled = StandardScaler().fit_transform(X_hc)

            obs_names = df_hc.index.astype(str).tolist() if obs_label == "Номер строки (Index)" else df_hc[obs_label].astype(str).tolist()
            var_names = [get_name(c) for c in hc_features]

            import matplotlib.pyplot as plt
            import seaborn as sns
            from scipy.cluster.hierarchy import dendrogram, linkage

            st.markdown("---")
            hc_plot_type = st.radio(
                "Выберите тип графика:",
                ["Кластеризация переменных (Шкал)", "Кластеризация наблюдений (Респондентов)", "Тепловая карта + Деревья (Clustergram)"], 
                horizontal=True
            )

            # 1. Дендрограмма шкал
            if hc_plot_type == "Кластеризация переменных (Шкал)":
                st.markdown("**Дендрограмма переменных:** показывает, какие психологические шкалы ведут себя похоже.")
                Z_vars = linkage(X_scaled.T, method='ward')
                fig_v, ax_v = plt.subplots(figsize=(10, 6))
                dendrogram(Z_vars, labels=var_names, leaf_rotation=45, leaf_font_size=10, ax=ax_v)
                plt.title("Дендрограмма (Шкалы)")
                plt.tight_layout()
                st.pyplot(fig_v)

            # 2. Дендрограмма людей
            elif hc_plot_type == "Кластеризация наблюдений (Респондентов)":
                st.markdown("**Дендрограмма наблюдений:** показывает, как респонденты объединяются в группы.")
                Z_obs = linkage(X_scaled, method='ward')
                fig_o, ax_o = plt.subplots(figsize=(12, 7))
                
                if len(obs_names) > 50:
                    dendrogram(Z_obs, labels=obs_names, leaf_rotation=90, leaf_font_size=8, ax=ax_o, truncate_mode='lastp', p=30, show_contracted=True)
                    plt.title("Дендрограмма (Респонденты) - Показаны 30 верхних узловых групп")
                else:
                    dendrogram(Z_obs, labels=obs_names, leaf_rotation=90, leaf_font_size=8, ax=ax_o)
                    plt.title("Дендрограмма (Респонденты)")
                    
                plt.tight_layout()
                st.pyplot(fig_o)

            # 3. Clustergram
            elif hc_plot_type == "Тепловая карта + Деревья (Clustergram)":
                st.markdown("**Clustergram:** объединяет обе дендрограммы и показывает выраженность признаков цветом.")
                df_cm = pd.DataFrame(X_scaled, index=obs_names, columns=var_names)
                fig_cm = sns.clustermap(
                    df_cm, method='ward', cmap='coolwarm', figsize=(10, 10),
                    yticklabels=True if len(obs_names) <= 50 else False,
                    xticklabels=True
                )
                st.pyplot(fig_cm.figure)


    # ---------------------------------------------------------
    # ПОД-ВКЛАДКА 2: K-MEANS С АВТО-ВЫБОРОМ
    # ---------------------------------------------------------
    with subtab_km:
        st.subheader("K-Means кластеризация с авто-определением")

        # Кнопки быстрого выбора для KM
        st.write("**Быстрое добавление шкал:**")
        km_b1, km_b2, km_b3, km_b4 = st.columns(4)
        km_b1.button("➕ Братусь", on_click=add_to_state, args=('km_sel', 'B_'), key="km_btn_b")
        km_b2.button("➕ Мильман", on_click=add_to_state, args=('km_sel', 'M_'), key="km_btn_m")
        km_b3.button("➕ ИПЛ", on_click=add_to_state, args=('km_sel', 'IPL_'), key="km_btn_i")
        km_b4.button("❌ Очистить", on_click=clear_state, args=('km_sel',), key="km_btn_clear")

        km_features = st.multiselect(
            "Признаки для кластеризации:",
            num_cols,
            key="km_sel",
            format_func=get_name
        )

        if len(km_features) >= 2:
            df_km = df.dropna(subset=km_features).copy()
            X_km = df_km[km_features]

            from sklearn.preprocessing import StandardScaler
            from sklearn.cluster import KMeans
            from sklearn.metrics import silhouette_score
            import plotly.graph_objects as go

            X_km_scaled = StandardScaler().fit_transform(X_km)

            # --- АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ (Индекс Силуэта) ---
            max_k = min(10, len(X_km) - 1)
            sil_scores = []
            K_range = range(2, max_k + 1)

            for k in K_range:
                km = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = km.fit_predict(X_km_scaled)
                sil_scores.append(silhouette_score(X_km_scaled, labels))

            best_k = K_range[np.argmax(sil_scores)]

            c_info1, c_info2 = st.columns([1, 2])
            with c_info1:
                st.success(f"**Оптимальное число кластеров:** {best_k}")
                st.caption("Рассчитано на основе максимума метрики Силуэта.")
                n_clusters = st.slider("Согласиться или выбрать вручную:", 2, max_k, int(best_k))
                run_btn = st.button("🚀 Запустить K-Means")

            with c_info2:
                fig_sil = go.Figure(data=go.Scatter(x=list(K_range), y=sil_scores, mode='lines+markers'))
                fig_sil.add_vline(x=best_k, line_dash="dash", line_color="green", annotation_text="Оптимум")
                fig_sil.update_layout(title="Метрика Силуэта (выше = лучше)", height=250, margin=dict(t=30, b=0))
                st.plotly_chart(fig_sil, use_container_width=True)

            if run_btn:
                res_clustered = run_clustering_analysis(df_km, km_features, n_clusters)

                if res_clustered is not None:
                    st.markdown("---")
                    
                    c_res1, c_res2 = st.columns(2)
                    with c_res1:
                        st.markdown("#### Карта кластеров (PCA)")
                        fig_pca = px.scatter(res_clustered, x='PC1', y='PC2', color='Cluster',
                                             title="Проекция групп на плоскость (2D)")
                        st.plotly_chart(fig_pca, use_container_width=True)

                    with c_res2:
                        st.markdown("#### Психологический профиль (Радар)")
                        cluster_means = res_clustered.groupby('Cluster')[km_features].mean().reset_index()
                        radar_features = [get_name(f) for f in km_features]

                        fig_radar = go.Figure()
                        for i, row in cluster_means.iterrows():
                            fig_radar.add_trace(go.Scatterpolar(
                                r=row[km_features].values,
                                theta=radar_features,
                                fill='toself',
                                name=f'Кластер {row["Cluster"]}'
                            ))
                        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), margin=dict(t=30, b=30))
                        st.plotly_chart(fig_radar, use_container_width=True)

                    st.markdown("#### Средние значения по группам")
                    st.dataframe(cluster_means.rename(columns={f: get_name(f) for f in km_features}).style.highlight_max(axis=0, color='lightgreen'))
# === TAB 6: ПСИХОМЕТРИКА ===
with tab6:
    st.header("📐 Психометрика (Надежность и Факторная структура)")
    st.warning("⚠️ **Аналитический контекст:** Так как в систему загружены финальные баллы по шкалам, мы исследуем **макро-структуру** (связи шкал между собой и выделение вторичных факторов), а не классическую надежность отдельных вопросов.")
    
    # --- Инициализация session_state для кнопок быстрого выбора ---
    if 'alpha_sel' not in st.session_state:
        st.session_state.alpha_sel = []
    if 'fa_sel' not in st.session_state:
        st.session_state.fa_sel = []

    # Функции-колбэки для добавления/очистки шкал
    def add_to_state_tab6(state_key, prefix):
        current = st.session_state[state_key]
        new_items = [c for c in num_cols if c.startswith(prefix) and c not in current]
        st.session_state[state_key] = current + new_items
    
    def clear_state_tab6(state_key):
        st.session_state[state_key] = []

    subtab_alpha, subtab_fa = st.tabs(["Внутренняя согласованность (Кронбах)", "Факторная структура (Главные компоненты)"])
    
    # ---------------------------------------------------------
    # 1. АЛЬФА КРОНБАХА (МАКРО-УРОВЕНЬ)
    # ---------------------------------------------------------
    with subtab_alpha:
        st.subheader("Макро-согласованность шкал (Альфа Кронбаха)")
        st.markdown("Позволяет проверить, образуют ли выбранные шкалы единый теоретический конструкт.")
        
        # Кнопки быстрого выбора
        st.write("**Быстрое добавление шкал:**")
        a_b1, a_b2, a_b3, a_b4 = st.columns(4)
        a_b1.button("➕ Братусь", on_click=add_to_state_tab6, args=('alpha_sel', 'B_'), key="btn_alpha_b")
        a_b2.button("➕ Мильман", on_click=add_to_state_tab6, args=('alpha_sel', 'M_'), key="btn_alpha_m")
        a_b3.button("➕ ИПЛ", on_click=add_to_state_tab6, args=('alpha_sel', 'IPL_'), key="btn_alpha_i")
        a_b4.button("❌ Очистить", on_click=clear_state_tab6, args=('alpha_sel',), key="btn_alpha_clear")

        alpha_cols = st.multiselect(
            "Выберите шкалы для проверки согласованности:", 
            num_cols, 
            key="alpha_sel",
            format_func=get_name
        )
        
        if len(alpha_cols) >= 2:
            df_alpha = df[alpha_cols].dropna()
            if not df_alpha.empty:
                alpha, ci = pg.cronbach_alpha(data=df_alpha)
                
                if alpha >= 0.8: interpretation = "Высокая (шкалы измеряют один общий супер-фактор)"
                elif alpha >= 0.7: interpretation = "Приемлемая (хорошая согласованность)"
                elif alpha >= 0.6: interpretation = "Сомнительная (слабая связь между шкалами)"
                else: interpretation = "Низкая (шкалы измеряют принципиально разные вещи)"
                
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    st.metric("Альфа Кронбаха (α)", f"{alpha:.3f}")
                    st.markdown(f"**Интерпретация:** {interpretation}")
                    st.caption(f"95% Доверительный интервал: [{ci[0]:.3f}, {ci[1]:.3f}]")
                with col_a2:
                    st.info("💡 **Как это понимать?** Если альфа высокая, значит респонденты отвечали на эти шкалы в едином ключе. Это позволяет объединить их в один комплексный индекс.")
            else:
                st.error("Недостаточно данных для расчета.")
        else:
            st.info("Выберите минимум 2 шкалы.")

    # ---------------------------------------------------------
    # 2. ФАКТОРНЫЙ АНАЛИЗ (МЕТОД ГЛАВНЫХ КОМПОНЕНТ)
    # ---------------------------------------------------------
    with subtab_fa:
        st.subheader("Извлечение скрытых факторов (PCA)")
        st.markdown("Показывает, как исходные шкалы группируются в укрупненные, скрытые (латентные) факторы.")
        
        # Кнопки быстрого выбора
        st.write("**Быстрое добавление шкал:**")
        f_b1, f_b2, f_b3, f_b4 = st.columns(4)
        f_b1.button("➕ Братусь", on_click=add_to_state_tab6, args=('fa_sel', 'B_'), key="btn_fa_b")
        f_b2.button("➕ Мильман", on_click=add_to_state_tab6, args=('fa_sel', 'M_'), key="btn_fa_m")
        f_b3.button("➕ ИПЛ", on_click=add_to_state_tab6, args=('fa_sel', 'IPL_'), key="btn_fa_i")
        f_b4.button("❌ Очистить", on_click=clear_state_tab6, args=('fa_sel',), key="btn_fa_clear")

        fa_cols = st.multiselect(
            "Выберите шкалы для факторного анализа:", 
            num_cols, 
            key="fa_sel",
            format_func=get_name
        )
        
        if len(fa_cols) >= 3:
            df_fa = df[fa_cols].dropna()
            
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(df_fa)
            
            pca_full = PCA()
            pca_full.fit(data_scaled)
            explained_variance = pca_full.explained_variance_ratio_ * 100
            
            col_fa1, col_fa2 = st.columns([1, 2])
            
            with col_fa1:
                eigenvalues = pca_full.explained_variance_
                kaiser_factors = sum(eigenvalues > 1.0)
                
                st.success(f"**Оптимально факторов (по Кайзеру):** {kaiser_factors}")
                n_factors = st.number_input("Сколько факторов извлечь?", min_value=1, max_value=len(fa_cols), value=max(1, int(kaiser_factors)))
            
            with col_fa2:
                fig_scree = go.Figure(data=go.Scatter(
                    x=list(range(1, len(fa_cols) + 1)), 
                    y=eigenvalues, 
                    mode='lines+markers',
                    name='Собственные значения'
                ))
                fig_scree.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Порог Кайзера (1.0)")
                fig_scree.update_layout(title="График 'Каменистой осыпи'", xaxis_title="Номер компоненты", yaxis_title="Собственное значение (Eigenvalue)", height=300)
                st.plotly_chart(fig_scree, use_container_width=True)

            pca_final = PCA(n_components=n_factors)
            pca_final.fit(data_scaled)
            
            loadings = pca_final.components_.T * np.sqrt(pca_final.explained_variance_)
            
            translated_fa_cols = [get_name(c) for c in fa_cols]
            factor_names = [f"Фактор {i+1} ({pca_final.explained_variance_ratio_[i]*100:.1f}%)" for i in range(n_factors)]
            
            fig_loadings = go.Figure(data=go.Heatmap(
                z=loadings,
                x=factor_names,
                y=translated_fa_cols,
                colorscale='RdBu_r',
                zmin=-1, zmax=1,
                text=np.round(loadings, 2),
                texttemplate="%{text}",
                hovertemplate="Шкала: %{y}<br>Фактор: %{x}<br>Нагрузка: %{z:.3f}<extra></extra>"
            ))
            
            fig_loadings.update_layout(title="Матрица факторных нагрузок (чем ближе к 1 или -1, тем сильнее связь)", height=max(400, len(fa_cols) * 35))
            st.plotly_chart(fig_loadings, use_container_width=True)
            
            st.caption("🔍 **Как читать матрицу:** Смотрите на значения по модулю > 0.4. Они показывают, какие оригинальные шкалы 'вошли' в состав нового скрытого фактора.")
            
        else:
            st.info("Для факторного анализа требуется минимум 3 шкалы.")
# === TAB 7: ПРЕДИКТИВНАЯ АНАЛИТИКА (Поиск драйверов) ===
with tab7:
    st.header("🔮 Поиск скрытых драйверов (Random Forest)")
    
    with st.expander("ℹ️ Как пользоваться этой вкладкой (Инструкция)"):
        st.markdown("""
        **Цель этой вкладки** — найти скрытые закономерности и понять, какие именно психологические факторы сильнее всего "драйвят" или тормозят конкретный показатель.

        **Шаг 1:** Выберите **Целевой показатель (Y)**. Это то, что вы хотите изучить.
        **Шаг 2:** Выберите **Факторы влияния (X)**. Это шкалы, среди которых алгоритм будет искать причины.
        
        ⚠️ **Правило чистоты данных:** Не пытайтесь предсказать *Общий балл* методики, используя в качестве факторов её же *Подшкалы*. 
        """)

    num_cols = df.select_dtypes(include=np.number).columns.tolist()

    c_pred1, c_pred2 = st.columns([1, 1.5])
    with c_pred1:
        target_var = st.selectbox(
            "🎯 Целевой показатель:", 
            num_cols, 
            index=num_cols.index('IPL_Total') if 'IPL_Total' in num_cols else 0,
            format_func=get_name
        )
        
    with c_pred2:
        st.markdown("**⚡ Быстрый выбор методик-предикторов:**")
        cb1, cb2, cb3 = st.columns(3)
        with cb1:
            sel_b = st.checkbox("Шкалы Братуся", value=True)
        with cb2:
            sel_m = st.checkbox("Шкалы Мильмана", value=False)
        with cb3:
            sel_ipl = st.checkbox("Шкалы ИПЛ", value=False)
            
        default_preds = []
        if sel_b:
            default_preds.extend([c for c in num_cols if c.startswith('B_') and c != target_var])
        if sel_m:
            default_preds.extend([c for c in num_cols if c.startswith('M_') and c != target_var])
        if sel_ipl:
            default_preds.extend([c for c in num_cols if c.startswith('IPL_') and c != target_var])

        predictor_vars = st.multiselect(
            "📈 Факторы влияния:",
            [c for c in num_cols if c != target_var],
            default=default_preds,
            format_func=get_name
        )

    if st.button("🚀 Найти ключевые драйверы"):
        if len(predictor_vars) < 2:
            st.warning("⚠️ Для обучения модели выберите хотя бы 2 фактора влияния.")
        else:
            with st.spinner("Обучаем модель Random Forest и вычисляем направления..."):
                df_pred = df[[target_var] + predictor_vars].dropna()
                
                if len(df_pred) < 15:
                    st.error("❌ Недостаточно данных для обучения.")
                else:
                    from sklearn.ensemble import RandomForestRegressor
                    from sklearn.metrics import r2_score
                    
                    X = df_pred[predictor_vars]
                    y = df_pred[target_var]
                    
                    rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
                    rf.fit(X, y)
                    r2 = r2_score(y, rf.predict(X))

                    # --- НОВЫЙ БЛОК: АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ НАПРАВЛЕНИЯ ---
                    dirs = []
                    for c in predictor_vars:
                        # Считаем линейную корреляцию фактора с целью
                        corr = df_pred[c].corr(df_pred[target_var])
                        if corr > 0:
                            dirs.append("📈") # Тянет вверх
                        else:
                            dirs.append("📉") # Тянет вниз (Блокатор)

                    importance = pd.DataFrame({
                        'Фактор': [get_name(c) for c in predictor_vars],
                        'Колонка': predictor_vars, 
                        'Важность': rf.feature_importances_ * 100,
                        'Знак': dirs
                    })
                    
                    # Создаем колонку с иконкой специально для отрисовки на графике
                    importance['Фактор_с_иконкой'] = importance['Знак'] + " " + importance['Фактор']
                    importance = importance.sort_values(by='Важность', ascending=True)

                    st.session_state['rf_results'] = {
                        'target_var': target_var,
                        'df_pred': df_pred,
                        'importance': importance,
                        'r2': r2,
                        'model': rf,
                        'features': predictor_vars
                    }

    if 'rf_results' in st.session_state:
        res = st.session_state['rf_results']
        t_var = res['target_var']
        df_p = res['df_pred']
        imp = res['importance']
        r_sq = res['r2']

        st.markdown("---")
        res_c1, res_c2 = st.columns([2, 1])

        with res_c1:
            st.markdown(f"#### 📊 Рейтинг влияния на «{get_name(t_var)}»")
            # Теперь используем 'Фактор_с_иконкой' для оси Y
            fig_rf = px.bar(
                imp, x='Важность', y='Фактор_с_иконкой', orientation='h',
                color='Важность', color_continuous_scale='Viridis'
            )
            fig_rf.update_layout(xaxis_title="Сила влияния (в %)", yaxis_title="", coloraxis_showscale=False, height=max(400, len(imp) * 35))
            st.plotly_chart(fig_rf, use_container_width=True, config={'displayModeBar': False})

        with res_c2:
            st.markdown("#### ⚙️ Качество модели")
            if r_sq > 0.5:
                st.success(f"**Точность объяснения (R²):** {r_sq*100:.1f}%")
            elif r_sq > 0.2:
                st.warning(f"**Точность (R²):** {r_sq*100:.1f}%")
            else:
                st.error(f"**Точность (R²):** {r_sq*100:.1f}%")

            st.markdown("---")
            st.markdown("🏆 **Топ-3 драйвера:**")
            top3 = imp.sort_values(by='Важность', ascending=False).head(3)
            for i, row in top3.iterrows():
                # Добавили вывод иконки прямо в текст Топ-3
                st.markdown(f"{row['Знак']} **{row['Фактор']}** ({row['Важность']:.1f}%)")

        st.markdown("---")
        st.markdown("### 🔍 Как именно работают Топ-3 драйвера?")
        st.markdown("`📈 Катализатор` (тянет вверх) | `📉 Блокатор` (тянет вниз)")
        
        graph_cols = st.columns(3)
        for idx, (index, row) in enumerate(top3.iterrows()):
            feat_name_icon = row['Фактор_с_иконкой']
            feat_col = row['Колонка']
            
            with graph_cols[idx]:
                fig_scatter = px.scatter(
                    df_p, x=feat_col, y=t_var, trendline="ols", trendline_color_override="red", opacity=0.7
                )
                fig_scatter.update_layout(
                    title=dict(text=f"№{idx+1}: {feat_name_icon}", font=dict(size=12)),
                    xaxis_title=row['Фактор'],
                    yaxis_title=get_name(t_var) if idx == 0 else "",
                    margin=dict(l=10, r=10, t=40, b=10),
                    height=300
                )
                st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

        st.markdown("### 🎛️ Проверить другие факторы")
        # Выпадающий список использует чистые имена шкал (без иконок) для удобства поиска
        ordered_features = imp.sort_values(by='Важность', ascending=False)['Фактор'].tolist()
        
        selected_feature_ru = st.selectbox(
            "Выберите любую шкалу из рейтинга для детального анализа:", 
            ordered_features
        )
        
        if selected_feature_ru:
            selected_row = imp[imp['Фактор'] == selected_feature_ru].iloc[0]
            selected_feature_col = selected_row['Колонка']
            icon = selected_row['Знак']
            
            fig_detail = px.scatter(
                df_p, x=selected_feature_col, y=t_var, trendline="ols", trendline_color_override="red",
                opacity=0.7, hover_data=df_p.columns
            )
            fig_detail.update_layout(
                title=dict(text=f"Взаимосвязь {icon}: {selected_feature_ru} ➔ {get_name(t_var)}", font=dict(size=16)),
                xaxis_title=selected_feature_ru, yaxis_title=get_name(t_var),
                margin=dict(l=20, r=20, t=50, b=20), height=450
            )
            st.plotly_chart(fig_detail, use_container_width=True)

        with st.expander("🧮 Как алгоритм рассчитывает проценты влияния?"):
           st.markdown("""
                        В основе расчетов лежит алгоритм **Random Forest Regressor (Случайный лес)**. Он не просто ищет линейные связи (как корреляция Пирсона), а способен находить сложную нелинейную логику.
                        
                        **Как это считается математически:**
                        1. **Построение деревьев:** Алгоритм строит 100 математических "деревьев решений". Каждое дерево пытается угадать Целевой показатель (Y), задавая вопросы к факторам влияния (X). Например: *"У этого человека балл по шкале 'Комфорт' больше 15 или меньше?"*
                        2. **Снижение ошибки (Variance Reduction):** Каждый раз, когда дерево разделяет людей на группы по какой-то шкале, алгоритм замеряет величину **MSE (Mean Squared Error)** — среднеквадратичную ошибку прогноза.
                        3. **Расчет важности узла:** Важность конкретной шкалы в одном разбиении вычисляется как разница между ошибкой до разделения и суммой ошибок после разделения: 
                           `Важность = Ошибка_до - (Доля_слева * Ошибка_слева + Доля_справа * Ошибка_справа)`
                        4. **Итоговый вес (Feature Importance):** Программа суммирует эту полезность для каждой шкалы по всем 100 деревьям. Затем эти суммы нормируются так, чтобы в сумме они давали **100%**.
                        
                        *Простыми словами:* Чем больший процент получила шкала, тем сильнее падала ошибка прогноза, когда компьютер использовал эту шкалу для классификации людей.
                        """)
# ==========================================
        # НОВЫЙ МОДУЛЬ: СИМУЛЯТОР "ЧТО-ЕСЛИ"
        # ==========================================
        st.markdown("---")
        st.markdown("### 🎛️ Симулятор «Что-если» (Интерактивный прогноз)")
        st.markdown("Смоделируйте идеального респондента! Изменяйте значения ползунками, а затем нажмите кнопку пересчета, чтобы увидеть новый прогноз.")

        if 'model' in res:
            rf_model = res['model']
            all_features = res['features']
            
            top5_cols = imp.sort_values(by='Важность', ascending=False).head(5)['Колонка'].tolist()
            
            sim_col1, sim_col2 = st.columns([1.5, 1])
            
            with sim_col1:
                st.markdown("#### Управление факторами (Топ-5)")
                # --- ОБЕРТКА В ФОРМУ (Блокирует автообновление) ---
                with st.form("simulator_form"):
                    user_inputs = {}
                    
                    for col in top5_cols:
                        col_name_ru = get_name(col)
                        min_val = float(df_p[col].min())
                        max_val = float(df_p[col].max())
                        mean_val = float(df_p[col].mean())
                        
                        user_inputs[col] = st.slider(
                            col_name_ru, 
                            min_value=min_val, max_value=max_val, value=mean_val, step=0.5
                        )
                    
                    # Кнопка отправки данных из формы
                    submit_sim = st.form_submit_button("🔄 Пересчитать прогноз")
            
            with sim_col2:
                sim_data = {}
                for col in all_features:
                    if col in user_inputs:
                        sim_data[col] = user_inputs[col]
                    else:
                        sim_data[col] = df_p[col].mean()
                
                df_sim = pd.DataFrame([sim_data])
                predicted_target = rf_model.predict(df_sim)[0]
                
                t_min = df_p[t_var].min()
                t_max = df_p[t_var].max()
                t_mean = df_p[t_var].mean()
                
                st.markdown(f"#### Прогноз: {get_name(t_var)}")
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=predicted_target,
                    delta={'reference': t_mean, 'position': "top"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Ожидаемый балл", 'font': {'size': 18}},
                    gauge={
                        'axis': {'range': [t_min, t_max], 'tickwidth': 1},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [t_min, t_mean], 'color': "lightgray"},
                            {'range': [t_mean, t_max], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': predicted_target
                        }
                    }
                ))
                fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
                
                # Обратная связь для пользователя
                if submit_sim:
                    st.success("Прогноз успешно обновлен!")
                else:
                    st.caption("Сдвиньте ползунки слева и нажмите «Пересчитать прогноз», чтобы обновить спидометр.")
# === TAB 8: ДЕТЕКТОР АНОМАЛИЙ (Isolation Forest) ===
with tab8:
    st.header("👽 Детектор аномалий (Изоляционный лес)")
    st.markdown("Поиск нетипичных респондентов с парадоксальными сочетаниями мотивов и смыслов.")
    
    with st.expander("ℹ️ Как это работает?"):
        st.markdown("""
        Алгоритм **Isolation Forest** ищет *многомерные* выбросы. 
        Например, высокий мотив 'Комфорт' — это нормально. Высокая 'Творческая активность' — тоже нормально. Но если у человека **оба** эти показателя зашкаливают (что психологически парадоксально), алгоритм пометит его как аномалию.
        """)
    
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    st.markdown("**1. Выберите шкалы для анализа на аномалии:**")
    cb_a1, cb_a2, cb_a3 = st.columns(3)
    with cb_a1: 
        sel_a_b = st.checkbox("Шкалы Братуся (Аномалии)", value=True)
    with cb_a2: 
        sel_a_m = st.checkbox("Шкалы Мильмана (Аномалии)", value=True)
    with cb_a3: 
        sel_a_ipl = st.checkbox("Шкалы ИПЛ (Аномалии)", value=False)
    
    anom_preds = []
    if sel_a_b: anom_preds.extend([c for c in num_cols if c.startswith('B_')])
    if sel_a_m: anom_preds.extend([c for c in num_cols if c.startswith('M_')])
    if sel_a_ipl: anom_preds.extend([c for c in num_cols if c.startswith('IPL_')])
    
    anom_vars = st.multiselect(
        "Анализируемые метрики:", anom_preds, default=anom_preds, format_func=get_name
    )
    
    contamination = st.slider(
        "Какой процент выборки считать 'странным' (чувствительность)?", 
        min_value=1, max_value=15, value=5, step=1
    )
    
    # КНОПКА ПОИСКА (Сохраняем результаты в память)
    if st.button("🔍 Найти аномалии", help="Запустить алгоритм Isolation Forest"):
        if len(anom_vars) < 2:
            st.warning("⚠️ Для поиска многомерных аномалий нужно выбрать хотя бы 2 шкалы.")
        else:
            with st.spinner("Прочесываем данные в поисках аномалий..."):
                df_anom = df.dropna(subset=anom_vars).copy()
                
                if len(df_anom) < 20:
                    st.error("❌ Слишком мало данных для обучения детектора.")
                else:
                    X_anom = df_anom[anom_vars]
                    
                    # Обучаем Изоляционный лес
                    iso = IsolationForest(contamination=contamination/100.0, random_state=42)
                    df_anom['Anomaly'] = iso.fit_predict(X_anom)
                    df_anom['Anomaly_Label'] = df_anom['Anomaly'].map({1: 'Норма', -1: 'Аномалия'})
                    df_anom['Anomaly_Score'] = iso.decision_function(X_anom) 
                    
                    # Создаем красивое имя для отображения
                    if 'FIO' in df_anom.columns:
                        df_anom['Display_Name'] = df_anom['FIO'].fillna("Аноним") + " (ID: " + df_anom.index.astype(str) + ")"
                    else:
                        df_anom['Display_Name'] = "Респондент ID: " + df_anom.index.astype(str)
                    
                    # PCA для графика
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X_anom)
                    pca_anom = PCA(n_components=2)
                    components = pca_anom.fit_transform(X_scaled)
                    
                    df_anom['PCA1'] = components[:, 0]
                    df_anom['PCA2'] = components[:, 1]
                    
                    # Запоминаем в session_state
                    st.session_state['anom_results'] = {
                        'df_anom': df_anom,
                        'anom_vars': anom_vars
                    }

    # ОТРИСОВКА ИНТЕРФЕЙСА (Берем данные из памяти)
    if 'anom_results' in st.session_state:
        res_a = st.session_state['anom_results']
        df_a = res_a['df_anom']
        a_vars = res_a['anom_vars']
        
        st.markdown("---")
        c_res1, c_res2 = st.columns([2, 1])
        
        with c_res1:
            st.markdown("#### 🌌 Карта респондентов (Проекция)")
            
            # ИСПРАВЛЕНИЕ ТУЛТИПА: Показываем только Имя, чтобы график не ломался
            fig_anom = px.scatter(
                df_a, x='PCA1', y='PCA2', color='Anomaly_Label',
                color_discrete_map={'Норма': '#3498db', 'Аномалия': '#e74c3c'},
                hover_name='Display_Name',
                hover_data={'PCA1': False, 'PCA2': False, 'Anomaly_Label': False},
                opacity=0.8
            )
            fig_anom.update_layout(
                title=dict(text="Красные точки — многомерные выбросы", font=dict(size=14)),
                xaxis_title="Скрытая компонента 1", yaxis_title="Скрытая компонента 2",
                legend_title="", margin=dict(l=10, r=10, t=40, b=10), height=400
            )
            fig_anom.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
            st.plotly_chart(fig_anom, use_container_width=True, config={'displayModeBar': False})
            
        with c_res2:
            num_anom = len(df_a[df_a['Anomaly'] == -1])
            st.metric("Найдено аномальных профилей", f"{num_anom} чел.")
            st.markdown("На графике слева ИИ сжал все выбранные шкалы в 2D-пространство. **Красные точки**, оторванные от синего облака — это респонденты с нетипичным мышлением.")
            st.caption("Наведите мышку на точку, чтобы увидеть, кто это.")
            
        st.markdown("#### 🕵️‍♂️ Досье на нетипичных респондентов")
        outliers = df_a[df_a['Anomaly'] == -1].sort_values('Anomaly_Score')
        
        if outliers.empty:
            st.success("При заданных настройках ярких аномалий не найдено. Выборка очень однородна.")
        else:
            # === НОВЫЙ БЛОК: РЕНТГЕН АНОМАЛИИ ===
            st.markdown("---")
            st.markdown("### 🔬 Рентген аномалии (В чем их странность?)")
            st.markdown("Выберите респондента из списка аномалий. Алгоритм сравнит его с «нормальной» частью выборки и покажет, какие шкалы у него зашкаливают.")
            
            selected_anom = st.selectbox("Выберите респондента для анализа:", outliers['Display_Name'].tolist())
            
            if selected_anom:
                # Берем данные выбранного человека
                person = outliers[outliers['Display_Name'] == selected_anom].iloc[0]
                
                # Берем всех "нормальных" людей для сравнения
                normal_df = df_a[df_a['Anomaly'] == 1]
                
                # Считаем Z-оценку (отклонение) по каждой выбранной шкале
                deviations = []
                for col in a_vars:
                    val = person[col]
                    mean_norm = normal_df[col].mean()
                    std_norm = normal_df[col].std()
                    
                    # Избегаем деления на ноль, если у всех нормальных одинаковый балл
                    z_score = (val - mean_norm) / std_norm if std_norm > 0 else 0
                        
                    deviations.append({
                        'Шкала': get_name(col),
                        'Балл респондента': val,
                        'Среднее по норме': round(mean_norm, 1),
                        'Отклонение (Z)': z_score,
                        'Абс_Отклонение': abs(z_score) # Для сортировки
                    })
                
                # Выбираем Топ-5 самых сильных отклонений
                dev_df = pd.DataFrame(deviations).sort_values(by='Абс_Отклонение', ascending=False).head(5)
                
                # Подготовка данных для красивого графика
                dev_df['Направление'] = dev_df['Отклонение (Z)'].apply(lambda x: 'Выше нормы' if x > 0 else 'Ниже нормы')
                
                fig_dev = px.bar(
                    dev_df, x='Отклонение (Z)', y='Шкала', orientation='h',
                    color='Направление',
                    color_discrete_map={'Выше нормы': '#27ae60', 'Ниже нормы': '#e74c3c'},
                    text='Балл респондента'
                )
                
                fig_dev.update_layout(
                    title=dict(text=f"Топ-5 экстремальных отклонений: {selected_anom}", font=dict(size=16)),
                    xaxis_title="Сила отклонения (в стандартных отклонениях Z)",
                    yaxis_title="",
                    height=350,
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                
                # Добавляем вертикальную линию нуля (норма)
                fig_dev.add_vline(x=0, line_width=2, line_color="black", opacity=0.5)
                
                st.plotly_chart(fig_dev, use_container_width=True, config={'displayModeBar': False})
                
                st.info("💡 **Как читать этот график:** Черная вертикальная линия (0) — это средний балл большинства людей. Зеленые столбцы показывают, что показатель человека аномально **завышен**. Красные — аномально **занижен**. Число на столбце — это сырой балл респондента по методике.")
            
            # Оставляем сырую таблицу в самом низу для выгрузки
            with st.expander("Посмотреть сырые данные всех аномальных респондентов (Таблица)"):
                cols_to_show = []
                if 'FIO' in df_a.columns: cols_to_show.append('FIO')
                if 'Gender' in df_a.columns: cols_to_show.append('Gender')
                cols_to_show.extend(a_vars)
                
                renamed_outliers = outliers[cols_to_show].rename(columns={c: get_name(c) for c in a_vars})
                st.dataframe(renamed_outliers, use_container_width=True)
# === TAB 9: СЕТЕВОЙ АНАЛИЗ (Network Psychometrics) ===
with tab9:
    st.header("🕸️ Сетевая психометрия (Графы связей)")
    st.markdown("Поиск корневых мотивов и смыслов. Личность представлена как нейросеть, где шкалы — это узлы, а корреляции — связи между ними.")

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    c_net1, c_net2 = st.columns([1.5, 1]) 
    with c_net1:
        st.markdown("**1. Выберите шкалы для построения сети:**")
        cb_n1, cb_n2, cb_n3 = st.columns(3)
        with cb_n1: 
            sel_n_b = st.checkbox("Шкалы Братуся (Сеть)", value=True)
        with cb_n2: 
            sel_n_m = st.checkbox("Шкалы Мильмана (Сеть)", value=True)
        with cb_n3: 
            sel_n_ipl = st.checkbox("Шкалы ИПЛ (Сеть)", value=False)
            
        net_preds = []
        if sel_n_b: net_preds.extend([c for c in num_cols if c.startswith('B_')])
        if sel_n_m: net_preds.extend([c for c in num_cols if c.startswith('M_')])
        if sel_n_ipl: net_preds.extend([c for c in num_cols if c.startswith('IPL_')])

        all_possible_vars = [c for c in num_cols if c.startswith('B_') or c.startswith('M_') or c.startswith('IPL_')]
        net_vars = st.multiselect(
            "Включить в сеть (можно редактировать точечно):", 
            all_possible_vars, default=net_preds, format_func=get_name
        )
    
    with c_net2:
        st.markdown("**2. Настройки чувствительности сети:**")
        threshold = st.slider(
            "Отсекать слабые связи (Порог корреляции |r|):", 
            min_value=0.1, max_value=0.8, value=0.3, step=0.05,
            help="Увеличьте порог, если граф похож на запутанный клубок ниток. Оставьте только самые сильные связи (>0.4)."
        )

    # --- КНОПКА ПОСТРОЕНИЯ (С сохранением в память) ---
    if st.button("🕸️ Построить нейросеть личности"):
        if len(net_vars) < 3:
            st.warning("⚠️ Для построения сети нужно выбрать минимум 3 шкалы.")
        else:
            with st.spinner("Рассчитываем топологию графа..."):
                df_net = df[net_vars].dropna()
                corr_matrix = df_net.corr()

                G = nx.Graph()
                for col in net_vars:
                    G.add_node(col, name=get_name(col))

                for i in range(len(net_vars)):
                    for j in range(i+1, len(net_vars)):
                        col1 = net_vars[i]
                        col2 = net_vars[j]
                        corr_val = corr_matrix.loc[col1, col2]
                        
                        if abs(corr_val) >= threshold:
                            G.add_edge(col1, col2, weight=abs(corr_val), corr=corr_val)

                isolated_nodes = list(nx.isolates(G))
                G.remove_nodes_from(isolated_nodes)

                if len(G.nodes) == 0:
                    st.error("❌ При таком высоком пороге корреляции не найдено ни одной связи. Снизьте порог.")
                else:
                    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
                    degrees = dict(G.degree())
                    
                    edge_traces = []
                    for edge in G.edges(data=True):
                        x0, y0 = pos[edge[0]]
                        x1, y1 = pos[edge[1]]
                        weight = edge[2]['weight']
                        corr = edge[2]['corr']
                        
                        line_color = '#2ecc71' if corr > 0 else '#e74c3c'
                        line_width = weight * 5 
                        
                        edge_trace = go.Scatter(
                            x=[x0, x1, None], y=[y0, y1, None],
                            line=dict(width=line_width, color=line_color),
                            hoverinfo='none', mode='lines', opacity=0.6
                        )
                        edge_traces.append(edge_trace)

                    node_x, node_y, node_text, node_hover, node_size = [], [], [], [], []
                    for node in G.nodes():
                        x, y = pos[node]
                        node_x.append(x)
                        node_y.append(y)
                        node_name = G.nodes[node]['name']
                        size = 20 + (degrees[node] * 5)
                        node_size.append(min(size, 60)) 
                        node_text.append(node_name)
                        node_hover.append(f"<b>{node_name}</b><br>Количество связей: {degrees[node]}")

                    node_trace = go.Scatter(
                        x=node_x, y=node_y, mode='markers+text', text=node_text,
                        textposition="top center", hoverinfo='text', hovertext=node_hover,
                        marker=dict(showscale=False, color='#3498db', size=node_size, line_width=2, line_color='white'),
                        textfont=dict(size=11, color="black")
                    )

                    fig_net = go.Figure(data=edge_traces + [node_trace],
                         layout=go.Layout(
                            title=dict(text="Топология мотивов и смыслов", font=dict(size=16)),
                            showlegend=False, hovermode='closest', margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            height=600, plot_bgcolor='white'
                        )
                    )
                    
                    # ЗАПОМИНАЕМ ГРАФ И ДАННЫЕ В ПАМЯТЬ
                    st.session_state['net_results'] = {
                        'fig_net': fig_net,
                        'G': G,
                        'degrees': degrees,
                        'isolated_nodes': isolated_nodes
                    }

    # --- ОТРИСОВКА ИНТЕРФЕЙСА (Берем данные из памяти) ---
    if 'net_results' in st.session_state:
        res_n = st.session_state['net_results']
        fig_net = res_n['fig_net']
        G = res_n['G']
        degrees = res_n['degrees']
        isolated_nodes = res_n['isolated_nodes']

        st.markdown("---")
        
        # 1. ЛЕГЕНДА ГРАФА
        st.markdown("### 🗺️ Легенда графа")
        st.markdown("""
        * 🟢 **Зеленые линии** — прямая связь (шкалы растут и падают синхронно, поддерживают друг друга).
        * 🔴 **Красные линии** — обратная связь (конфликт мотивов: одна шкала растет, другая падает).
        * 🔵 **Размер кружка** — чем больше узел, тем больше у него связей (это Центральный смыслообразующий мотив).
        """)

        # 2. ОТРИСОВКА ГРАФА И КНОПКА СКАЧИВАНИЯ (PNG)
        # Включаем верхнюю панель инструментов Plotly (displayModeBar: True)
        st.plotly_chart(fig_net, use_container_width=True, config={
            'displayModeBar': True,
            'toImageButtonOptions': {'format': 'png', 'filename': 'Network_Graph', 'scale': 3}
        })
        st.caption("👆 Наведите мышку в правый верхний угол графика и нажмите на иконку фотоаппарата, чтобы скачать граф как картинку (PNG).")

        # 3. КНОПКА СКАЧИВАНИЯ (HTML)
        # Генерируем HTML файл из графика
        html_bytes = fig_net.to_html(include_plotlyjs='cdn').encode('utf-8')
        st.download_button(
            label="💾 Скачать этот граф как интерактивный файл (HTML)",
            data=html_bytes,
            file_name="psychometric_network.html",
            mime="text/html",
            help="Вы скачаете файл, который можно открыть в любом браузере. В нем можно приближать узлы и смотреть связи даже без Python!"
        )

        # 4. АНАЛИТИКА ГРАФА
        st.markdown("### 🏆 Аналитика графа")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            max_degree_node = max(degrees, key=degrees.get)
            st.info(f"**Центральный хаб (Смыслообразующий мотив):**\n\n🎯 {G.nodes[max_degree_node]['name']} (Связей: {degrees[max_degree_node]})")
        with res_col2:
            st.success(f"**Характеристики сети:**\n\n* Активных узлов: {len(G.nodes)}\n* Сильных связей: {len(G.edges)}\n* Изолированных шкал отсеяно: {len(isolated_nodes)}")

        # 5. ДЕТАЛЬНЫЙ АНАЛИЗ УЗЛА (Новая функция)
        st.markdown("---")
        st.markdown("### 🔍 Детальный анализ связей")
        st.markdown("Выберите любую шкалу из графа, чтобы посмотреть точный список всех её связей и их силу.")

        # Получаем список всех узлов в графе (по алфавиту)
        node_names = sorted([G.nodes[n]['name'] for n in G.nodes()])
        selected_node_name = st.selectbox("Шкала для детального анализа:", node_names)

        if selected_node_name:
            # Находим технический ключ выбранного узла
            node_key = [n for n in G.nodes() if G.nodes[n]['name'] == selected_node_name][0]
            
            # Достаем все ребра (связи), подключенные к этому узлу
            edges = G.edges(node_key, data=True)
            
            edge_data = []
            for u, v, data in edges:
                # Определяем, кто "сосед"
                target_key = v if u == node_key else u
                target_name = G.nodes[target_key]['name']
                corr_val = data['corr']
                
                edge_data.append({
                    'Связанная шкала': target_name,
                    'Сила связи (Коэффициент r)': round(corr_val, 3),
                    'Тип связи': '🟢 Прямая (Синхронная)' if corr_val > 0 else '🔴 Обратная (Конфликтная)',
                    'Абсолютная сила': abs(corr_val) # Скрытая колонка для правильной сортировки
                })
                
            if edge_data:
                # Переводим в DataFrame, сортируем от самых сильных связей к слабым и удаляем техническую колонку
                df_edges = pd.DataFrame(edge_data).sort_values(by='Абсолютная сила', ascending=False).drop(columns=['Абсолютная сила'])
                st.dataframe(df_edges, use_container_width=True)
            else:
                st.info("У этой шкалы нет сильных связей при текущем пороге.")