// ФУНКЦИИ ТЕСТА IPL - ИННОВАЦИОННЫЙ ПОТЕНЦИАЛ

function setupIPLTest() {
  // Инициализация теста IPL
  renderIPLQuestions();
  initIPLTest();
}

function renderIPLQuestions() {
  const container = document.getElementById('ipl-container');
  if (!container) return;

  // Очистка контейнера
  container.innerHTML = '';

  // Создание вопросов
  ipl_qs.forEach((question, qIndex) => {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'form-group';
    questionDiv.innerHTML = `
      <h3>${qIndex + 1}. ${question}</h3>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
        ${[1, 2, 3, 4, 5].map(value => `
          <div class="option-card">
            <input type="radio" name="ipl_q${qIndex}" id="ipl_${qIndex}_${value}" value="${value}" onchange="handleIPLAnswer(${qIndex}, ${value})">
            <label for="ipl_${qIndex}_${value}" style="flex:1; cursor:pointer; text-align:center;">${value}</label>
          </div>
        `).join('')}
      </div>
    `;
    container.appendChild(questionDiv);
  });
}

function handleIPLAnswer(qIndex, value) {
  state.iplAnswers[qIndex] = parseInt(value);
  validateIPLAnswers();
  saveStateToLocal();
}

function validateIPLAnswers() {
  // Проверяем, все ли вопросы отвечены
  let allAnswered = true;
  const unanswered = [];

  for (let i = 0; i < ipl_qs.length; i++) {
    if (!state.iplAnswers[i]) {
      allAnswered = false;
      unanswered.push(i);
    }
  }

  // Обновляем UI для непройденных вопросов
  ipl_qs.forEach((_, qIndex) => {
    const questionElement = document.querySelector(`[name="ipl_q${qIndex}"]`)?.closest('.form-group');
    if (questionElement) {
      questionElement.classList.toggle('highlight-error', !state.iplAnswers[qIndex]);
    }
  });

  // Обновляем сообщение об ошибке
  const errorDiv = document.getElementById('ipl-error');
  if (errorDiv) {
    errorDiv.style.display = allAnswered ? 'none' : 'block';
  }

  return allAnswered;
}

function initIPLTest() {
  // Инициализация начального состояния
  if (!state.iplAnswers) {
    state.iplAnswers = {};
  }

  // Восстанавливаем выбранные ответы
  Object.keys(state.iplAnswers).forEach(qIndex => {
    const value = state.iplAnswers[qIndex];
    const radio = document.getElementById(`ipl_${qIndex}_${value}`);
    if (radio) {
      radio.checked = true;
    }
  });

  validateIPLAnswers();
}

function prevIPL() {
  goToStep('milman');
}

function finishSurvey() {
  if (validateIPLAnswers()) {
    // Переход к результатам
    goToStep('loading');
    setTimeout(() => {
      processResults();
      goToStep('results');
      displayResults();
    }, 1500); // Имитация обработки результатов
  }
}

// Функции обработки результатов IPL
function calculateIPLResults() {
  // Рассчитываем результаты теста IPL
  // Разделение на шкалы по инструкции
  const scales = {
    anxiety: [26, 32, 33, 34, 35], // Тревожность
    adaptation: [27, 28, 29, 30, 31], // Адаптивность
    empathy: [39, 40, 41, 42, 43], // Эмпатия
    initiative: [44, 45, 46, 47, 48], // Инициативность
    risk: [2, 3, 9, 10, 18], // Склонность к риску
    conformism: [12, 13, 14, 16, 17], // Конформизм
    flexibility: [20, 21, 22, 23, 24], // Интеллектуальная гибкость
    control: [5, 19, 25, 36, 37], // Контроль
    optimism: [1, 6, 7, 8, 11], // Оптимизм
    selfesteem: [4, 15, 38, 49, 50] // Самооценка
  };

  const results = {};

  // Рассчитываем баллы для каждой шкалы
  Object.keys(scales).forEach(scale => {
    const questions = scales[scale];
    let sum = 0;
    let count = 0;

    questions.forEach(qNum => {
      // Индекс в массиве начинается с 0, а вопросы нумеруются с 1
      const qIndex = qNum - 1;
      if (state.iplAnswers[qIndex] !== undefined) {
        // Некоторые вопросы обратные (например: 5, 13, 14, 16, 17, 19, 25, 33, 34, 35)
        const isReverse = [5, 14, 15, 17, 18, 20, 26, 34, 35, 36].includes(qNum);
        
        if (isReverse) {
          sum += (6 - state.iplAnswers[qIndex]); // Обратная оценка (5 становится 1, 4 становится 2 и т.д.)
        } else {
          sum += state.iplAnswers[qIndex];
        }
        count++;
      }
    });

    results[scale] = count > 0 ? sum / count : 0; // Среднее значение
  });

  return results;
}

function interpretIPLResults(results) {
  // Интерпретация результатов IPL
  const interpretations = {};

  // Тревожность
  if (results.anxiety > 3.5) {
    interpretations.anxiety = "Повышенный уровень тревожности может снижать инновационный потенциал";
  } else if (results.anxiety < 2.5) {
    interpretations.anxiety = "Низкий уровень тревожности способствует открытости новому";
  } else {
    interpretations.anxiety = "Средний уровень тревожности";
  }

  // Адаптивность
  if (results.adaptation > 3.5) {
    interpretations.adaptation = "Высокая адаптивность позволяет эффективно приспосабливаться к изменениям";
  } else if (results.adaptation < 2.5) {
    interpretations.adaptation = "Низкая адаптивность может затруднять восприятие изменений";
  } else {
    interpretations.adaptation = "Средняя адаптивность";
  }

  // Эмпатия
  if (results.empathy > 3.5) {
    interpretations.empathy = "Высокий уровень эмпатии способствует командной работе и коммуникации";
  } else if (results.empathy < 2.5) {
    interpretations.empathy = "Низкий уровень эмпатии может ограничивать взаимодействие с другими";
  } else {
    interpretations.empathy = "Средний уровень эмпатии";
  }

  // Инициативность
  if (results.initiative > 3.5) {
    interpretations.initiative = "Высокий уровень инициативности - важный фактор инновационного поведения";
  } else if (results.initiative < 2.5) {
    interpretations.initiative = "Низкая инициативность может препятствовать проявлению новаторства";
  } else {
    interpretations.initiative = "Средний уровень инициативности";
  }

  // Склонность к риску
  if (results.risk > 3.5) {
    interpretations.risk = "Высокая готовность к риску способствует инновационной деятельности";
  } else if (results.risk < 2.5) {
    interpretations.risk = "Низкая готовность к риску может ограничивать инновационное поведение";
  } else {
    interpretations.risk = "Средняя готовность к риску";
  }

  // Конформизм
  if (results.conformism > 3.5) {
    interpretations.conformism = "Высокий уровень конформизма может ограничивать нестандартное мышление";
  } else if (results.conformism < 2.5) {
    interpretations.conformism = "Низкий уровень конформизма способствует независимости мышления";
  } else {
    interpretations.conformism = "Средний уровень конформизма";
  }

  // Интеллектуальная гибкость
  if (results.flexibility > 3.5) {
    interpretations.flexibility = "Высокая интеллектуальная гибкость способствует генерации новых идей";
  } else if (results.flexibility < 2.5) {
    interpretations.flexibility = "Низкая интеллектуальная гибкость может ограничивать креативность";
  } else {
    interpretations.flexibility = "Средняя интеллектуальная гибкость";
  }

  // Контроль
  if (results.control > 3.5) {
    interpretations.control = "Высокий уровень контроля может способствовать реализации инноваций";
  } else if (results.control < 2.5) {
    interpretations.control = "Низкий уровень контроля может затруднять реализацию идей";
  } else {
    interpretations.control = "Средний уровень контроля";
  }

  // Оптимизм
  if (results.optimism > 3.5) {
    interpretations.optimism = "Высокий уровень оптимизма способствует положительному восприятию перемен";
  } else if (results.optimism < 2.5) {
    interpretations.optimism = "Низкий уровень оптимизма может снижать мотивацию к инновациям";
  } else {
    interpretations.optimism = "Средний уровень оптимизма";
  }

  // Самооценка
  if (results.selfesteem > 3.5) {
    interpretations.selfesteem = "Высокая самооценка способствует уверенности в новых начинаниях";
  } else if (results.selfesteem < 2.5) {
    interpretations.selfesteem = "Низкая самооценка может ограничивать уверенность в инновационной деятельности";
  } else {
    interpretations.selfesteem = "Средняя самооценка";
  }

  return interpretations;
}