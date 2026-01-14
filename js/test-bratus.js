// ФУНКЦИИ ТЕСТА БРАТУСА - ЖИЗНЕННЫЕ ЦЕННОСТИ

function setupBratusTest() {
  // Инициализация теста Братуса
  renderBratusOptions();
  initBratusRanking();
}

function renderBratusOptions() {
  const container = document.getElementById('bratus-options');
  if (!container) return;

  // Очистка контейнера
  container.innerHTML = '';

  // Создание карточек опций
  bratus_stmts.forEach(stmt => {
    const card = document.createElement('div');
    card.className = 'option-card';
    card.innerHTML = `
      <input type="checkbox" id="bratus_${stmt.id}" onchange="handleBratusSelection(${stmt.id})">
      <label for="bratus_${stmt.id}" style="flex:1; cursor:pointer;">${stmt.t}</label>
    `;
    container.appendChild(card);
  });
}

function handleBratusSelection(id) {
  const checkbox = document.getElementById(`bratus_${id}`);
  const isChecked = checkbox.checked;

  // Обновление состояния выбора
  const existingIndex = state.bratusRanks.findIndex(item => item.id === id);
  
  if (isChecked && existingIndex === -1) {
    // Добавляем элемент в текущий ранг
    const currentRank = getCurrentBratusRank();
    state.bratusRanks.push({ id, rank: currentRank });
  } else if (!isChecked && existingIndex !== -1) {
    // Удаляем элемент из списка
    state.bratusRanks.splice(existingIndex, 1);
  }

  updateBratusUI();
  saveStateToLocal();
}

function getCurrentBratusRank() {
  // Возвращаем номер текущего ранга (1-8)
  // Считаем, сколько рангов уже заполнено
  const ranks = [...new Set(state.bratusRanks.map(item => item.rank))];
  return Math.min(ranks.length + 1, 8);
}

function updateBratusUI() {
  // Обновляем UI в соответствии с текущим состоянием
  const selectedCount = state.bratusRanks.filter(item => item.rank === getCurrentBratusRank()).length;
  const subText = document.getElementById('bratus-sub');
  
  if (subText) {
    const currentRank = getCurrentBratusRank();
    subText.textContent = `Выберите ${getRankText(currentRank)} (${selectedCount}/3)`;
  }
  
  // Обновляем состояние чекбоксов
  bratus_stmts.forEach(stmt => {
    const checkbox = document.getElementById(`bratus_${stmt.id}`);
    if (checkbox) {
      const isSelected = state.bratusRanks.some(item => item.id === stmt.id);
      checkbox.checked = isSelected;
      
      // Обновляем класс карточки
      const card = checkbox.parentElement;
      if (card) {
        card.classList.toggle('checked', isSelected);
      }
    }
  });
  
  // Обновляем сообщение об ошибке
  const errorDiv = document.getElementById('bratus-error');
  if (errorDiv) {
    const currentRankItems = state.bratusRanks.filter(item => item.rank === getCurrentBratusRank());
    errorDiv.style.display = currentRankItems.length !== 3 ? 'block' : 'none';
  }
}

function getRankText(rank) {
  // Возвращает текст для текущего ранга
  const rankTexts = [
    'первые 3 самых важных',
    'следующие 3 важных',
    'следующие 3',
    'следующие 3',
    'следующие 3',
    'следующие 3',
    'следующие 3',
    'оставшиеся 3'
  ];
  return rankTexts[rank - 1] || `ещё 3`;
}

function nextBratusRank() {
  const currentRank = getCurrentBratusRank();
  const currentRankItems = state.bratusRanks.filter(item => item.rank === currentRank);
  
  if (currentRankItems.length !== 3) {
    document.getElementById('bratus-error').style.display = 'block';
    return;
  }
  
  if (currentRank >= 8) {
    // Переход к следующему этапу
    goToStep('milman');
  } else {
    // Просто обновляем UI для следующего ранга
    updateBratusUI();
  }
}

function prevBratusRank() {
  const currentRank = getCurrentBratusRank();
  
  if (currentRank > 1) {
    // Удаляем элементы текущего ранга
    state.bratusRanks = state.bratusRanks.filter(item => item.rank < currentRank);
    updateBratusUI();
  } else {
    // Переход к предыдущему шагу
    goToStep('form');
  }
}

function initBratusRanking() {
  // Инициализация начального состояния
  if (state.bratusRanks.length === 0) {
    state.bratusRanks = [];
  }
  updateBratusUI();
}