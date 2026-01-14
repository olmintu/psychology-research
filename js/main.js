// ГЛАВНЫЙ ФАЙЛ ЛОГИКИ ПРИЛОЖЕНИЯ

// Состояние приложения
let state = {
  currentStep: 'form',
  formData: {},
  bratusRanks: [],
  milmanAnswers: {},
  iplAnswers: {},
  anonMode: false
};

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
  loadStateFromLocal();
  updateUI();
  initializeEventListeners();
});

// Функции управления интерфейсом
function updateUI() {
  // Скрыть все шаги
  document.querySelectorAll('.step').forEach(step => {
    step.classList.remove('active');
  });
  
  // Показать текущий шаг
  const currentStepElement = document.getElementById(`step-${state.currentStep}`);
  if(currentStepElement) {
    currentStepElement.classList.add('active');
  }
  
  // Обновить прогресс
  updateProgressBar();
}

function updateProgressBar() {
  const progressBar = document.getElementById('progress');
  if(!progressBar) return;
  
  let progress = 0;
  switch(state.currentStep) {
    case 'form':
      progress = 10;
      break;
    case 'bratus':
      progress = 35;
      break;
    case 'milman':
      progress = 60;
      break;
    case 'ipl':
      progress = 85;
      break;
    case 'results':
      progress = 100;
      break;
  }
  
  progressBar.style.width = `${progress}%`;
}

function initializeEventListeners() {
  // Инициализация обработчиков событий
  setupBratusTest();
  setupMilmanTest();
  setupIPLTest();
}

// Основные функции приложения
function toggleAnon() {
  state.anonMode = document.getElementById('anon_mode').checked;
  document.getElementById('anon_warning').style.display = state.anonMode ? 'block' : 'none';
  updateFormVisibility();
  saveStateToLocal();
}

function updateFormVisibility() {
  const formElements = ['fio', 'gender', 'age', 'family_status', 'children', 'is_working', 'work_place', 'has_secondary_edu', 'edu_status', 'university', 'speciality', 'edu_level', 'edu_basis', 'course'];
  const requiredMarkers = document.querySelectorAll('.req');
  
  formElements.forEach(id => {
    const element = document.getElementById(id);
    if(element) {
      if(state.anonMode) {
        element.disabled = true;
        element.required = false;
      } else {
        element.disabled = false;
        if(['fio', 'gender', 'age', 'family_status', 'children', 'is_working', 'has_secondary_edu', 'edu_status'].includes(id)) {
          element.required = true;
        }
      }
    }
  });
  
  requiredMarkers.forEach(marker => {
    marker.style.display = state.anonMode ? 'none' : 'inline';
  });
}

function validateForm() {
  if(state.anonMode) {
    goToStep('bratus');
    return;
  }
  
  const requiredFields = ['fio', 'gender', 'age', 'family_status', 'children', 'is_working', 'has_secondary_edu', 'edu_status'];
  let isValid = true;
  
  requiredFields.forEach(fieldId => {
    const field = document.getElementById(fieldId);
    if(!field || !field.value.trim()) {
      isValid = false;
      field?.classList.add('highlight-error');
    } else {
      field?.classList.remove('highlight-error');
    }
  });
  
  // Проверка корректности возраста
  const ageField = document.getElementById('age');
  if(ageField && ageField.value) {
    const age = parseInt(ageField.value);
    if(isNaN(age) || age < 14 || age > 100) {
      isValid = false;
      ageField.classList.add('highlight-error');
    } else {
      ageField.classList.remove('highlight-error');
    }
  }
  
  document.getElementById('form-error').style.display = isValid ? 'none' : 'block';
  
  if(isValid) {
    collectFormData();
    goToStep('bratus');
  }
}

function collectFormData() {
  state.formData = {
    fio: document.getElementById('fio').value,
    gender: document.getElementById('gender').value,
    age: document.getElementById('age').value,
    family_status: document.getElementById('family_status').value,
    children: document.getElementById('children').value,
    is_working: document.getElementById('is_working').value,
    work_place: document.getElementById('work_place').value,
    has_secondary_edu: document.getElementById('has_secondary_edu').value,
    edu_status: document.getElementById('edu_status').value,
    university: document.getElementById('university').value,
    speciality: document.getElementById('speciality').value,
    edu_level: document.getElementById('edu_level').value,
    edu_basis: document.getElementById('edu_basis').value,
    course: document.getElementById('course').value,
    anonMode: state.anonMode
  };
}

function goToStep(stepName) {
  state.currentStep = stepName;
  updateUI();
  saveStateToLocal();
}

// Функции сохранения и загрузки состояния
function saveStateToLocal() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch(e) {
    console.error("Ошибка сохранения в localStorage:", e);
  }
}

function loadStateFromLocal() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if(saved) {
      state = {...state, ...JSON.parse(saved)};
    }
  } catch(e) {
    console.error("Ошибка загрузки из localStorage:", e);
  }
}

function clearState() {
  localStorage.removeItem(STORAGE_KEY);
  location.reload();
}

// Функции для разработки (DEV MODE)
function checkDevMode(value) {
  if(value === "dev") {
    document.getElementById('dev-panel').style.display = 'block';
  }
}

function fillRandomData() {
  // Заполнение случайными данными для тестирования
  document.getElementById('fio').value = 'Иванов Иван';
  document.getElementById('gender').value = 'Мужской';
  document.getElementById('age').value = '25';
  document.getElementById('family_status').value = 'Женат/Замужем';
  document.getElementById('children').value = 'Да';
  document.getElementById('is_working').value = 'Да';
  document.getElementById('work_place').value = 'ООО Ромашка';
  document.getElementById('has_secondary_edu').value = 'Да';
  document.getElementById('edu_status').value = 'Закончил';
  document.getElementById('university').value = 'МГУ';
  document.getElementById('speciality').value = 'Психология';
  document.getElementById('edu_level').value = 'Магистратура';
  document.getElementById('edu_basis').value = 'Бюджет';
  document.getElementById('course').value = '4';
  
  updateFormVisibility();
  saveStateToLocal();
}

function loadDevJSON() {
  const jsonInput = document.getElementById('dev-json-input').value;
  try {
    const parsed = JSON.parse(jsonInput);
    state = {...state, ...parsed};
    updateUI();
    document.getElementById('dev-error').textContent = '';
  } catch(e) {
    document.getElementById('dev-error').textContent = 'Неверный формат JSON';
  }
}

// Функция переключения деталей
function toggleDetails(targetId) {
  const target = document.getElementById(targetId);
  const button = event.target.closest('.toggle-details');
  
  if(target) {
    const isVisible = target.style.display !== 'none';
    target.style.display = isVisible ? 'none' : 'block';
    
    if(button) {
      button.setAttribute('aria-expanded', !isVisible);
    }
  }
}

// Функции тестов будут подключены из отдельных файлов