// ФУНКЦИИ ТЕСТА МИЛМАНА - СТРУКТУРА МОТИВАЦИИ

function setupMilmanTest() {
  // Инициализация теста Милмана
  renderMilmanQuestions();
  initMilmanTest();
}

function renderMilmanQuestions() {
  const container = document.getElementById('milman-container');
  if (!container) return;

  // Очистка контейнера
  container.innerHTML = '';

  // Создание вопросов
  milman_qs.forEach((question, qIndex) => {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'form-group';
    questionDiv.innerHTML = `
      <h3>${qIndex + 1}. ${question.q}</h3>
      ${question.i.map((item, iIndex) => `
        <div class="option-card">
          <input type="radio" name="milman_q${qIndex}" id="milman_${qIndex}_${iIndex}" value="${iIndex + 1}" onchange="handleMilmanAnswer(${qIndex}, ${iIndex + 1})">
          <label for="milman_${qIndex}_${iIndex}" style="flex:1; cursor:pointer;">${item}</label>
        </div>
      `).join('')}
    `;
    container.appendChild(questionDiv);
  });
}

function handleMilmanAnswer(qIndex, value) {
  state.milmanAnswers[qIndex] = value;
  validateMilmanAnswers();
  saveStateToLocal();
}

function validateMilmanAnswers() {
  // Проверяем, все ли вопросы отвечены
  let allAnswered = true;
  const unanswered = [];

  for (let i = 0; i < milman_qs.length; i++) {
    if (!state.milmanAnswers[i]) {
      allAnswered = false;
      unanswered.push(i);
    }
  }

  // Обновляем UI для непройденных вопросов
  milman_qs.forEach((_, qIndex) => {
    const questionElement = document.querySelector(`[name="milman_q${qIndex}"]`)?.closest('.form-group');
    if (questionElement) {
      questionElement.classList.toggle('highlight-error', !state.milmanAnswers[qIndex]);
    }
  });

  // Обновляем сообщение об ошибке
  const errorDiv = document.getElementById('milman-error');
  if (errorDiv) {
    errorDiv.style.display = allAnswered ? 'none' : 'block';
  }

  return allAnswered;
}

function initMilmanTest() {
  // Инициализация начального состояния
  if (!state.milmanAnswers) {
    state.milmanAnswers = {};
  }

  // Восстанавливаем выбранные ответы
  Object.keys(state.milmanAnswers).forEach(qIndex => {
    const value = state.milmanAnswers[qIndex];
    const radio = document.getElementById(`milman_${qIndex}_${value - 1}`);
    if (radio) {
      radio.checked = true;
    }
  });

  validateMilmanAnswers();
}

function finishMilman() {
  if (validateMilmanAnswers()) {
    goToStep('ipl');
  }
}

function prevMilman() {
  goToStep('bratus');
}

// Функции обработки результатов Милмана
function calculateMilmanResults() {
  // Рассчитываем результаты теста Милмана
  const lifeReal = [0, 0, 0, 0]; // Жизнь - Реальное (вопросы 1, 3, 5, 7)
  const lifeIdeal = [0, 0, 0, 0]; // Жизнь - Идеальное (вопросы 2, 4, 6, 8)
  const workReal = [0, 0, 0, 0]; // Работа - Реальное (вопросы 9, 11, 13, 15)
  const workIdeal = [0, 0, 0, 0]; // Работа - Идеальное (вопросы 10, 12, 14, 16)

  // Обработка ответов на вопросы
  for (let i = 0; i < milman_qs.length; i++) {
    const answer = state.milmanAnswers[i];
    if (answer) {
      // Индекс для массивов (0-3)
      const idx = Math.floor(i / 2) % 4;
      
      if ([0, 2, 4, 6].includes(i)) { // Реальное для жизни
        lifeReal[idx] += answer;
      } else if ([1, 3, 5, 7].includes(i)) { // Идеальное для жизни
        lifeIdeal[idx] += answer;
      } else if ([8, 10, 12, 14].includes(i)) { // Реальное для работы
        workReal[idx] += answer;
      } else if ([9, 11, 13, 15].includes(i)) { // Идеальное для работы
        workIdeal[idx] += answer;
      }
    }
  }

  // Нормализация значений (масштабирование от 1 до 5)
  const normalize = (arr) => arr.map(val => val / 4); // Предполагаем, что по 4 вопроса в каждой категории

  return {
    lifeReal: normalize(lifeReal),
    lifeIdeal: normalize(lifeIdeal),
    workReal: normalize(workReal),
    workIdeal: normalize(workIdeal),
    emotionalProfile: calculateEmotionalProfile()
  };
}

function calculateEmotionalProfile() {
  // Рассчитываем эмоциональный профиль
  // Основывается на ответах на вопросы 13-16 (отношение к неудачам и стрессу)
  const stressResponses = [];
  for (let i = 12; i < 16; i++) {
    if (state.milmanAnswers[i]) {
      stressResponses.push(state.milmanAnswers[i]);
    }
  }

  // Простой расчет на основе среднего значения
  const avgResponse = stressResponses.reduce((sum, val) => sum + val, 0) / stressResponses.length;
  
  return {
    avgResponse: avgResponse || 0,
    stability: 6 - avgResponse // Чем выше ответ, тем ниже стабильность (1-5 шкала)
  };
}