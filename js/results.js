// ФУНКЦИИ ОТОБРАЖЕНИЯ РЕЗУЛЬТАТОВ

function processResults() {
  // Обработка результатов всех тестов
  state.results = {
    bratus: calculateBratusResults(),
    milman: calculateMilmanResults(),
    ipl: calculateIPLResults()
  };
}

function calculateBratusResults() {
  // Рассчитываем результаты теста Братуса
  const categorySums = {
    hedonistic: 0,    // Гедонистические (3, 11, 19)
    status: 0,        // Статусные (5, 13, 21)
    communicative: 0, // Коммуникативные (6, 14, 22)
    family: 0,        // Семейные (7, 15, 23)
    existential: 0,   // Экзистенциальные (10, 16, 18)
    cognitive: 0,     // Когнитивные (8, 17, 24)
    altruistic: 0,    // Альтруистические (1, 9, 12)
    selfrealization: 0 // Самореализация (4, 12, 20) - примечание: 12 используется дважды
  };

  // Обработка рангов
  state.bratusRanks.forEach(item => {
    const stmt = bratus_stmts.find(s => s.id === item.id);
    if (stmt) {
      // Определяем категорию по ID
      if ([3, 11, 19].includes(item.id)) {
        categorySums.hedonistic += item.rank;
      } else if ([5, 13, 21].includes(item.id)) {
        categorySums.status += item.rank;
      } else if ([6, 14, 22].includes(item.id)) {
        categorySums.communicative += item.rank;
      } else if ([7, 15, 23].includes(item.id)) {
        categorySums.family += item.rank;
      } else if ([10, 16, 18].includes(item.id)) {
        categorySums.existential += item.rank;
      } else if ([8, 17, 24].includes(item.id)) {
        categorySums.cognitive += item.rank;
      } else if ([1, 9, 20].includes(item.id)) { // Исправлено: 12 -> 20 для самореализации
        categorySums.altruistic += item.rank;
      } else if ([4, 12, 20].includes(item.id)) {
        categorySums.selfrealization += item.rank;
      }
    }
  });

  // Нормализация: делим на количество утверждений в категории (3) и инвертируем
  Object.keys(categorySums).forEach(key => {
    categorySums[key] = 9 - (categorySums[key] / 3); // 9 = максимальный ранг (1-8) + 1
  });

  return categorySums;
}

function displayResults() {
  // Отображение результатов пользователю
  displayBratusResults();
  displayMilmanResults();
  displayIPLResults();
  generateResultText();
}

function displayBratusResults() {
  const container = document.getElementById('textBratus');
  if (!container) return;

  const results = state.results.bratus;
  const categories = [
    { key: 'hedonistic', name: 'Гедонистические смыслы', desc: 'Основаны на потребности получать удовольствие от жизни, быть счастливым, наслаждаться эмоциями и ощущениями.' },
    { key: 'status', name: 'Статусные смыслы', desc: 'Основаны на потребности занимать высокое положение в обществе, строить карьеру, добиваться успеха и признания.' },
    { key: 'communicative', name: 'Коммуникативные смыслы', desc: 'Основаны на потребности общаться с другими людьми, переживать эмоции общения, чувствовать свою нужность.' },
    { key: 'family', name: 'Семейные смыслы', desc: 'Основаны на потребности заботиться о семье, жить ради нее, передавать лучшее детям.' },
    { key: 'existential', name: 'Экзистенциальные смыслы', desc: 'Основаны на потребности придавать ценность жизни, иметь свободу выбора, испытывать любовь.' },
    { key: 'cognitive', name: 'Когнитивные смыслы', desc: 'Основаны на потребности познавать жизнь, разбираться в противоречиях мира и собственной личности.' },
    { key: 'altruistic', name: 'Альтруистические смыслы', desc: 'Основаны на потребности бескорыстно помогать другим, делать добро, служить общему благу.' },
    { key: 'selfrealization', name: 'Смыслы самореализации', desc: 'Основаны на потребности исполнить предназначение, реализовать способности и совершенствовать личность.' }
  ];

  // Сортировка по важности (по возрастанию ранга - более важные)
  const sortedCategories = [...categories].sort((a, b) => results[b.key] - results[a.key]);

  let content = '<table><tr><th>Сфера</th><th>Важность</th><th>Интерпретация</th></tr>';
  sortedCategories.forEach(cat => {
    const score = results[cat.key];
    const level = getImportanceLevel(score);
    content += `
      <tr>
        <td data-label="Сфера">${cat.name}</td>
        <td data-label="Важность"><span class="score-badge ${getScoreClass(score)}">${score.toFixed(1)}</span></td>
        <td data-label="Интерпретация">${cat.desc}</td>
      </tr>
    `;
  });
  content += '</table>';

  container.innerHTML = content;
}

function getImportanceLevel(score) {
  if (score >= 7) return 'очень высокая';
  if (score >= 5) return 'высокая';
  if (score >= 3) return 'средняя';
  return 'низкая';
}

function getScoreClass(score) {
  if (score >= 6) return 'bg-green';
  if (score >= 4) return 'bg-blue';
  return 'bg-red';
}

function displayMilmanResults() {
  const container = document.getElementById('textMilman');
  if (!container) return;

  const results = state.results.milman;

  // Генерация диаграммы для результатов Милмана
  drawMilmanChart(results);

  let content = `
    <h3>Жизнь: Идеал vs Реальность</h3>
    <p>Сравнение ваших установок на идеальное и реальное в жизни:</p>
    <ul>
      <li>Реально: ${results.lifeReal.map((val, idx) => `Шкала ${idx+1}: ${val.toFixed(1)}`).join(', ')}</li>
      <li>Идеально: ${results.lifeIdeal.map((val, idx) => `Шкала ${idx+1}: ${val.toFixed(1)}`).join(', ')}</li>
    </ul>

    <h3>Работа/Учёба: Идеал vs Реальность</h3>
    <p>Сравнение ваших установок на идеальное и реальное в профессиональной сфере:</p>
    <ul>
      <li>Реально: ${results.workReal.map((val, idx) => `Шкала ${idx+1}: ${val.toFixed(1)}`).join(', ')}</li>
      <li>Идеально: ${results.workIdeal.map((val, idx) => `Шкала ${idx+1}: ${val.toFixed(1)}`).join(', ')}</li>
    </ul>

    <h3>Эмоциональный профиль</h3>
    <p>Уровень эмоциональной устойчивости: ${results.emotionalProfile.stability.toFixed(1)} из 5</p>
    <p>Средняя реакция на стресс: ${results.emotionalProfile.avgResponse.toFixed(1)} из 5</p>
  `;

  container.innerHTML = content;
}

function drawMilmanChart(results) {
  const ctx = document.getElementById('chartMilman');
  if (!ctx) return;

  // Удаление существующего графика, если он есть
  if (window.milmanChart) {
    window.milmanChart.destroy();
  }

  // Подготовка данных для графика
  const labels = ['Жизнь (Реал)', 'Жизнь (Идеал)', 'Работа (Реал)', 'Работа (Идеал)'];
  const realValues = [(results.lifeReal.reduce((a,b) => a+b, 0)/results.lifeReal.length), 
                     (results.lifeIdeal.reduce((a,b) => a+b, 0)/results.lifeIdeal.length),
                     (results.workReal.reduce((a,b) => a+b, 0)/results.workReal.length),
                     (results.workIdeal.reduce((a,b) => a+b, 0)/results.workIdeal.length)];

  window.milmanChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Уровень выраженности',
        data: realValues,
        backgroundColor: [
          'rgba(52, 152, 219, 0.7)',
          'rgba(46, 204, 113, 0.7)',
          'rgba(155, 89, 182, 0.7)',
          'rgba(241, 196, 15, 0.7)'
        ],
        borderColor: [
          'rgba(52, 152, 219, 1)',
          'rgba(46, 204, 113, 1)',
          'rgba(155, 89, 182, 1)',
          'rgba(241, 196, 15, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 5
        }
      }
    }
  });
}

function displayIPLResults() {
  const container = document.getElementById('iplDetails');
  if (!container) return;

  const results = state.results.ipl;
  const interpretations = interpretIPLResults(results);

  let content = `
    <h3>Результаты по шкалам</h3>
    <table>
      <tr><th>Шкала</th><th>Балл</th><th>Интерпретация</th></tr>
      <tr>
        <td data-label="Шкала">Тревожность</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(5-results.anxiety)}">${results.anxiety.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.anxiety}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Адаптивность</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.adaptation)}">${results.adaptation.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.adaptation}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Эмпатия</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.empathy)}">${results.empathy.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.empathy}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Инициативность</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.initiative)}">${results.initiative.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.initiative}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Склонность к риску</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.risk)}">${results.risk.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.risk}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Конформизм</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(5-results.conformism)}">${results.conformism.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.conformism}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Интеллектуальная гибкость</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.flexibility)}">${results.flexibility.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.flexibility}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Контроль</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.control)}">${results.control.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.control}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Оптимизм</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.optimism)}">${results.optimism.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.optimism}</td>
      </tr>
      <tr>
        <td data-label="Шкала">Самооценка</td>
        <td data-label="Балл"><span class="score-badge ${getScoreClass(results.selfesteem)}">${results.selfesteem.toFixed(2)}</span></td>
        <td data-label="Интерпретация">${interpretations.selfesteem}</td>
      </tr>
    </table>
  `;

  container.innerHTML = content;
}

function generateResultText() {
  // Генерация текста результата для скачивания
  const resultArea = document.getElementById('result-area');
  if (!resultArea) return;

  const text = `Результаты психологического исследования

Участник: ${state.formData.fio || (state.anonMode ? "Анонимный участник" : "Данные отсутствуют")}
Дата: ${new Date().toLocaleDateString('ru-RU')}

ТЕСТ 1: Жизненные смыслы (Братус)
-----------------------------------
${Object.entries(state.results.bratus).map(([key, value]) => `${key}: ${value.toFixed(2)}`).join('\n')}

ТЕСТ 2: Структура мотивации (Милман)
-------------------------------------
Жизнь (реальное): ${state.results.milman.lifeReal.join(', ')}
Жизнь (идеальное): ${state.results.milman.lifeIdeal.join(', ')}
Работа (реальное): ${state.results.milman.workReal.join(', ')}
Работа (идеальное): ${state.results.milman.workIdeal.join(', ')}
Эмоциональный профиль: устойчивость ${state.results.milman.emotionalProfile.stability.toFixed(2)}, реакция на стресс ${state.results.milman.emotionalProfile.avgResponse.toFixed(2)}

ТЕСТ 3: Инновационный потенциал (IPL)
--------------------------------------
${Object.entries(state.results.ipl).map(([key, value]) => `${key}: ${value.toFixed(2)}`).join('\n')}

Все данные обработаны и сохранены.`;

  resultArea.value = text;
}

function downloadJSON() {
  // Создание JSON с результатами
  const data = {
    formData: state.formData,
    bratusRanks: state.bratusRanks,
    milmanAnswers: state.milmanAnswers,
    iplAnswers: state.iplAnswers,
    results: state.results,
    timestamp: new Date().toISOString()
  };

  const jsonStr = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonStr], {type: 'application/json'});
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = `результаты-${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();

  setTimeout(() => {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
}

function copyResult() {
  const resultArea = document.getElementById('result-area');
  if (resultArea) {
    resultArea.style.display = 'block';
    resultArea.select();
    document.execCommand('copy');
    
    const copyMsg = document.getElementById('copy-msg');
    if (copyMsg) {
      copyMsg.style.display = 'block';
      setTimeout(() => {
        copyMsg.style.display = 'none';
      }, 2000);
    }
  }
}