// --- ИНИЦИАЛИЗАЦИЯ ТЕМЫ ---
function initTheme() {
    const savedTheme = localStorage.getItem('app_theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // Если в ОС стоит темная тема, ставим ее по умолчанию
        document.documentElement.setAttribute('data-theme', 'dark');
    }
}
initTheme(); // Вызываем сразу, чтобы не было "белой вспышки" при загрузке
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('app_theme', newTheme);
    
    // Перерисовываем графики Мильмана, если они открыты, чтобы обновить цвет текста (сделаем это позже)
}
function showSoftAskModal() {
document.getElementById('soft-ask-modal').style.display = 'flex';
}
function closeSoftAskAndFill() {
// Пользователь согласился дозаполнить. Закрываем окно и подсвечиваем поля.
document.getElementById('soft-ask-modal').style.display = 'none';
document.getElementById('age').style.borderColor = "var(--warning)";
document.getElementById('gender').style.borderColor = "var(--warning)";
document.getElementById('gender').focus();
}
function proceedAsCompleteAnon() {
// Пользователь отказался наотрез. Закрываем окно и пускаем дальше.
document.getElementById('soft-ask-modal').style.display = 'none';

// Снимаем возможную подсветку
document.getElementById('age').style.borderColor = "#ddd";
document.getElementById('gender').style.borderColor = "#ddd";

saveStateToLocal();
switchStep('step-form', 'step-bratus');
renderBratus();
}
// --- КОНФИГУРАЦИЯ ---
const GOOGLE_URL = "https://script.google.com/macros/s/AKfycbyBH_ksIaHmQxklthf1SgxzmhxAPkqABdkTFTin1TObQJZ98DudLE_20IbqEHR-SKaqCg/exec";
const STORAGE_KEY = "survey_state_v10";
// Состояние
let state = { meta: {}, bratus: {}, rank: 1, milman: {}, ipl: {}, timing: {start: Date.now(), milman_start:0, ipl_start:0} };
let anonMode = false;
// --- PERSISTENCE ---
function saveStateToLocal() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); updateProgress(); }
function loadStateFromLocal() {
let saved = localStorage.getItem(STORAGE_KEY);
if (saved) Object.assign(state, JSON.parse(saved));
}
function clearState() { localStorage.removeItem(STORAGE_KEY); window.location.reload(); }

// Запускаем инициализацию после загрузки страницы
window.addEventListener('DOMContentLoaded', initUserImporter);
// INIT
window.onload = function() {
if (localStorage.getItem(STORAGE_KEY)) {
    loadStateFromLocal();
    if (state.finished) {
        finishSurvey(true);
    } else if (Object.keys(state.ipl).length > 0) {
        switchStep('step-form', 'step-ipl'); renderIPL();
    } else if (Object.keys(state.milman).length > 0) {
        switchStep('step-form', 'step-milman'); renderMilman();
    } else if (state.rank > 1 || (state.bratus && Object.keys(state.bratus).length > 0)) {
        switchStep('step-form', 'step-bratus'); renderBratus();
    } else if (state.meta.fio) {
        restoreForm();
    }
}
};
function restoreForm() {
if (state.meta.mode === 'anon' || state.meta.fio === "Аноним") {
    document.getElementById('anon_mode').checked = true;
    toggleAnon();
}
for(let k in state.meta) { let el = document.getElementById(k); if(el) el.value = state.meta[k]; }
toggleWorkPlace(); toggleEduBlock(); toggleKmnsName();
}
function updateProgress() {
let progressFill = document.getElementById('progress');
let progressBarContainer = document.querySelector('.progress-bar');
// 1. Считаем реальные ответы пользователя
let bratusCount = Object.keys(state.bratus).length; // Максимум 8
let milmanCount = Object.keys(state.milman).length; // Максимум 112
let iplCount = Object.keys(state.ipl).length;       // Максимум 36
let totalSteps = 8 + 112 + 36; // Всего 156
let currentSteps = bratusCount + milmanCount + iplCount;
let pct = (currentSteps / totalSteps) * 100;
// На стартовом экране сбрасываем в 0
if (document.getElementById('step-form').classList.contains('active') || currentSteps === 0) {
    pct = 0;
} else if (pct < 2) {
    pct = 2; // Чтобы было видно начало на первом вопросе
}
// 2. Устанавливаем ширину
progressFill.style.width = pct + "%";
// 3. Красим в зеленый, если ответил на ВСЕ вопросы
if (pct >= 100) {
    progressFill.style.backgroundColor = "var(--success)"; // Зеленый
} else {
    progressFill.style.backgroundColor = "var(--primary)"; // Синий
}
// 4. Прячем бар на экране результатов
// Используем setTimeout, чтобы дождаться окончания анимации switchStep (200мс)
setTimeout(() => {
    if (document.getElementById('step-results').classList.contains('active')) {
        progressBarContainer.style.display = 'none';
    } else {
        progressBarContainer.style.display = 'block';
    }
}, 250);
checkSmartButtons();
}
function checkSmartButtons() {
// 1. Братусь (Ждем ровно 3 галочки)
let bratusBtn = document.querySelector('#step-bratus .btn-container');
if (bratusBtn) {
    let checkedCount = document.querySelectorAll('#bratus-options input:checked').length;
    if (checkedCount === 3) bratusBtn.classList.add('smart-sticky');
    else bratusBtn.classList.remove('smart-sticky');
}
// 2. Мильман (Ждем 112 ответов: 14 вопросов * 8 вариантов)
let milmanBtn = document.querySelector('#step-milman .btn-container');
if (milmanBtn) {
    if (Object.keys(state.milman).length === 112) milmanBtn.classList.add('smart-sticky');
    else milmanBtn.classList.remove('smart-sticky');
}
// 3. ИПЛ (Ждем 36 ответов)
let iplBtn = document.querySelector('#step-ipl .btn-container');
if (iplBtn) {
    if (Object.keys(state.ipl).length === 36) iplBtn.classList.add('smart-sticky');
    else iplBtn.classList.remove('smart-sticky');
}
}
// --- GOD MODE (DEV) ---
function checkDevMode(val) {
if(val.toLowerCase().trim() === 'dev') {
    document.getElementById('dev-panel').style.display = 'block';
}
}
function fillRandomData() {
state.meta = { fio: "Тестовый Юзер", gender: "Мужской", age: "25", family_status: "Холост/Не замужем", children: "Нет", is_working: "Да", work_place: "IT", has_secondary_edu: "Нет", edu_status: "Учусь", university: "СурГУ", speciality: "Психология", edu_level: "Бакалавриат", edu_basis: "Бюджет", course: "4", mode: "dev" };

let ids = Array.from({length:24}, (_, i) => i + 1);
for(let r=1; r<=8; r++) {
    state.bratus[r] = [];
    for(let k=0; k<3; k++) {
        let randIdx = Math.floor(Math.random() * ids.length);
        state.bratus[r].push(ids[randIdx]);
        ids.splice(randIdx, 1);
    }
}
state.rank = 8;
for(let q=0; q<14; q++) for(let i=0; i<8; i++) state.milman[`${q}_${i}`] = Math.floor(Math.random() * 4);
for(let i=0; i<36; i++) state.ipl[i] = Math.floor(Math.random() * 5) + 1;

saveStateToLocal();
finishSurvey();
}
function loadDevJSON() {
try {
    let json = document.getElementById('dev-json-input').value;
    let data = JSON.parse(json);
    if(data.bratus && data.milman && data.ipl) {
        state = data;
        state.meta.mode = "dev"; // Force dev to avoid pollution
        saveStateToLocal();
        finishSurvey(true);
    } else {
        alert("Некорректный JSON (нет полей bratus/milman/ipl)");
    }
} catch(e) {
    document.getElementById('dev-error').innerText = "Ошибка парсинга: " + e.message;
}
}
// --- ЛОГИКА ---
function toggleAnon() {
anonMode = document.getElementById('anon_mode').checked;
state.meta.mode = anonMode ? 'anon' : 'normal';
document.getElementById('anon_warning').style.display = anonMode ? 'block' : 'none';
document.querySelectorAll('.req').forEach(el => el.style.display = anonMode ? 'none' : 'inline');
const inputs = document.querySelectorAll('#step-form input:not(#anon_mode), #step-form select');
inputs.forEach(el => el.style.backgroundColor = anonMode ? 'var(--bg)' : 'var(--input-bg)');
saveStateToLocal();
}
function toggleWorkPlace() { document.getElementById('work_place_block').style.display = (document.getElementById('is_working').value === "Да") ? 'block' : 'none'; }
function toggleEduBlock() {
const status = document.getElementById('edu_status').value;
document.getElementById('edu_block').style.display = (status === "Учусь" || status === "Закончил") ? 'block' : 'none';
document.getElementById('course_block').style.display = (status === "Учусь") ? 'block' : 'none';
}
function toggleKmnsName() {
const isKmns = document.getElementById('is_kmns').value === "Да";
document.getElementById('kmns_name_block').style.display = isKmns ? 'block' : 'none';
// Если выбрали "Нет", очищаем поле, чтобы не отправлять старое значение
if (!isKmns) {
    document.getElementById('kmns_name').value = "";
}
}
function validateForm() {
// --- DEV-РЕЖИМ  ---
let rawFio = document.getElementById('fio');
if (rawFio && rawFio.value.toLowerCase().trim() === 'dev') {
    const devBtn = document.getElementById('dev-autofill-btn');
    if(devBtn) devBtn.style.display = 'block';
}
// 1. Формируем список актуальных полей в зависимости от статуса обучения
let ids = ['fio','gender','age','is_kmns','family_status','children','is_working','has_secondary_edu','edu_status'];
const status = document.getElementById('edu_status').value;
if(status === 'Учусь') ids = ids.concat(['university','speciality','edu_level','edu_basis','course']);
else if(status === 'Закончил') ids = ids.concat(['university','speciality','edu_level','edu_basis']);

let valid = true;
anonMode = document.getElementById('anon_mode').checked;

if (!anonMode) {
    // --- ОБЫЧНЫЙ РЕЖИМ --- (Строгая проверка всех полей)
    ids.forEach(id => {
        let el = document.getElementById(id);
        if(!el || !el.value) { 
            if(el) el.style.borderColor = "var(--error)"; 
            valid = false; 
        } else { 
            if(el) el.style.borderColor = "#ddd"; 
            state.meta[id] = el.value; 
        }
    });
    
    // Сохраняем kmns_name (оно необязательное в обычном режиме)
    let kmnsEl = document.getElementById('kmns_name');
    state.meta['kmns_name'] = (kmnsEl && kmnsEl.value.trim() !== "") ? kmnsEl.value : "";
    
    if(!valid) { 
        document.getElementById('form-error').style.display = 'block'; 
        return; // Прерываемся, просим дозаполнить
    }
} else {
    // --- АНОНИМНЫЙ РЕЖИМ --- (Сохраняем всё, что ввели, остальное - "Аноним")
    ids.forEach(id => {
        let el = document.getElementById(id);
        // Если поле существует, имеет значение и это не пустая строка
        if (el && el.value && el.value.trim() !== "") {
            state.meta[id] = el.value; // Сохраняем реальные данные
        } else {
            state.meta[id] = "Аноним"; // Заполняем пустоты
        }
        if(el) el.style.borderColor = "#ddd"; // Убираем красные рамки, если были
    });
    // Защита от дурака: принудительно стираем ФИО в анонимном режиме
    state.meta['fio'] = "Аноним"; 
    
    // Сохраняем kmns_name
    let kmnsEl = document.getElementById('kmns_name');
    state.meta['kmns_name'] = (kmnsEl && kmnsEl.value && kmnsEl.value.trim() !== "") ? kmnsEl.value : "Аноним";
    // --- ЛОГИКА "SOFT ASK" (Мягкая просьба) ---
    // Проверяем, заполнил ли аноним наши самые главные поля (пол и возраст)
    let ageVal = state.meta['age'];
    let genderVal = state.meta['gender'];
    
    if (ageVal === "Аноним" || genderVal === "Аноним") {
        // Если нет — показываем окно с просьбой (которое мы обсуждали в шагах 2 и 3)
        showSoftAskModal();
        return; // Прерываем переход, пока не нажмут кнопку в модалке
    }
}
// Если всё ок (или Soft Ask уже пройден), идем дальше
document.getElementById('form-error').style.display = 'none';
saveStateToLocal();
switchStep('step-form', 'step-bratus');
renderBratus();
}
function renderBratus() {
const c = document.getElementById('bratus-options'); c.innerHTML = "";
document.getElementById('bratus-sub').innerHTML = `Выберите <b>3</b> утверждения для <b>${state.rank}-го места</b>`;

let used = []; 
for(let k in state.bratus) if(parseInt(k) !== state.rank) used = used.concat(state.bratus[k]);

bratus_stmts.forEach(s => {
    if(!used.includes(s.id)) {
        let div = document.createElement('div'); div.className = 'option-card'; div.innerHTML = `<input type="checkbox" value="${s.id}"> ${s.t}`;
        if(state.bratus[state.rank] && state.bratus[state.rank].includes(s.id)) { div.classList.add('checked'); div.querySelector('input').checked = true; }
        div.onclick = (e) => { 
            if(e.target.tagName!=='INPUT') div.querySelector('input').click(); 
            div.classList.toggle('checked', div.querySelector('input').checked); 
            saveStateToLocal();
        };
        div.querySelector('input').onchange = () => saveStateToLocal();
        c.appendChild(div);
    }
});
updateProgress();
}
function nextBratusRank() {
const ch = document.querySelectorAll('#bratus-options input:checked');
if(ch.length !== 3) { document.getElementById('bratus-error').style.display = 'block'; return; }
document.getElementById('bratus-error').style.display = 'none';
state.bratus[state.rank] = Array.from(ch).map(i => parseInt(i.value));
saveStateToLocal();
if(state.rank < 8) { state.rank++; renderBratus(); window.scrollTo(0,0); }
else { state.timing.milman_start = Date.now(); switchStep('step-bratus', 'step-milman'); renderMilman(); }
}
function prevBratusRank() { if(state.rank > 1) { state.rank--; renderBratus(); } else switchStep('step-bratus', 'step-form'); saveStateToLocal(); }
function renderMilman() {
const c = document.getElementById('milman-container');
if(c.innerHTML) {
    for(let k in state.milman) { 
        let el = document.querySelector(`input[name="m_${k}"][value="${state.milman[k]}"]`); 
        if(el) el.checked = true; 
        let row = document.getElementById('row_m_' + k);
        if(row) row.classList.add('answered');
    }
    return; 
}
milman_qs.forEach((q, qi) => {
    let h = `<div class="q-block"><h3>${qi+1}. ${q.q}</h3><table><thead><tr><th>Утверждение</th><th>Да, согласен</th><th>Пожалуй согласен </th><th>Когда как</th><th>Нет / Не знаю</th></tr></thead><tbody>`;
    q.i.forEach((txt, ii) => {
        let nm = `m_${qi}_${ii}`;
        h += `<tr id="row_${nm}"><td>${txt}</td>
        <td data-label="Да"><input type="radio" name="${nm}" value="3" onclick="saveM('${nm}',3)"></td>
        <td data-label="Пожалуй"><input type="radio" name="${nm}" value="2" onclick="saveM('${nm}',2)"></td>
        <td data-label="Когда как"><input type="radio" name="${nm}" value="1" onclick="saveM('${nm}',1)"></td>
        <td data-label="Нет/Не знаю"><input type="radio" name="${nm}" value="0" onclick="saveM('${nm}',0)"></td></tr>`;
    });
    c.innerHTML += h + "</tbody></table></div>";
});
for(let k in state.milman) { 
    let el = document.querySelector(`input[name="m_${k}"][value="${state.milman[k]}"]`); 
    if(el) el.checked = true; 
    let row = document.getElementById('row_m_' + k);
    if(row) row.classList.add('answered');
}
updateProgress();
}
function saveM(k, v) { 
state.milman[k.replace('m_','')] = v; 
let row = document.getElementById('row_'+k);
row.classList.remove('highlight-error'); 
row.classList.add('answered');
saveStateToLocal(); 
}
function finishMilman() {
if(!validateGroup('m', 14, 8)) return;

// Check for Fast Clicker (less than 90s)
if (state.timing && state.timing.milman_start) {
    let dur = (Date.now() - state.timing.milman_start) / 1000;
    if (dur < 90) {
        state.meta.flags = (state.meta.flags || "") + "FAST_MILMAN;";
    }
}
state.timing.ipl_start = Date.now();
switchStep('step-milman', 'step-ipl');
renderIPL();
}
function prevMilman() { switchStep('step-milman', 'step-bratus'); saveStateToLocal(); }
function renderIPL() {
const c = document.getElementById('ipl-container');
if(c.innerHTML) {
    for(let k in state.ipl) { 
        let el = document.querySelector(`input[name="ipl_${k}"][value="${state.ipl[k]}"]`); 
        if(el) el.checked = true; 
        let row = document.getElementById('row_ipl_' + k);
        if(row) row.classList.add('answered');
    }
    return;
}
let h = `<table><thead><tr><th>Утверждение</th><th>Не согласен</th><th>Скорее не согласен</th><th>Сложно сказать</th><th>Скорее согласен</th><th>Согласен</th></tr></thead><tbody>`;
ipl_qs.forEach((txt, i) => {
    let nm = `ipl_${i}`;
    const mobileLabels = ["Нет", "Скорее нет", "Не знаю", "Скорее да", "Да"]; 
    h += `<tr id="row_${nm}"><td>${i+1}. ${txt}</td>${[1,2,3,4,5].map((v, idx) => `<td data-label="${mobileLabels[idx]}"><input type="radio" name="${nm}" value="${v}" onclick="saveI(${i},${v})"></td>`).join('')}</tr>`;
});
c.innerHTML = h + "</tbody></table>";
for(let k in state.ipl) { 
    let el = document.querySelector(`input[name="ipl_${k}"][value="${state.ipl[k]}"]`); 
    if(el) el.checked = true; 
    let row = document.getElementById('row_ipl_' + k);
    if(row) row.classList.add('answered');
}
updateProgress();
}
function saveI(i, v) { 
state.ipl[i] = v; 
let row = document.getElementById('row_ipl_'+i);
row.classList.remove('highlight-error'); 
row.classList.add('answered');
saveStateToLocal(); 
}
function prevIPL() { switchStep('step-ipl', 'step-milman'); saveStateToLocal(); }
// --- ФИНАЛ ---
function finishSurvey(skipFetch = false) {
if(!skipFetch && !validateGroup('ipl', 36, 1)) return;
state.finished = true; 
//Расчет итогового времени
state.timing.end = Date.now(); 
let total_sec = Math.round((state.timing.end - state.timing.start) / 1000);
let m = Math.floor(total_sec / 60);
let s = total_sec % 60;
// Формат ММ.СС (с добавлением ведущего нуля для секунд, например 10.05)
state.timing.total_formatted = m + "." + (s < 10 ? "0" : "") + s;
// Проверка Fast Clicker для ИПЛ ---
if (state.timing && state.timing.ipl_start) {
    let durIPL = (Date.now() - state.timing.ipl_start) / 1000;
    if (durIPL < 60) { // Если 36 вопросов пройдены быстрее 60 сек
        state.meta.flags = (state.meta.flags || "") + "FAST_IPL;";
    }
}
saveStateToLocal();
updateProgress();
if(skipFetch) {
    switchStep('step-ipl', 'step-results'); 
    switchStep('step-form', 'step-results'); 
    calculateAndShowResults(true);
    return;
}
switchStep('step-ipl', 'step-loading');
const isDev = state.meta.mode === 'dev';
if (!isDev) {
    // Создаем глобальную функцию для отправки, чтобы вызывать её по кнопке повторно
    window.retryCloudSync = function() {
        document.getElementById('final-msg').innerHTML = "⏳ Отправка данных в облако...";
        fetch(GOOGLE_URL, { method: "POST", mode: "no-cors", headers: { "Content-Type": "application/json" }, body: JSON.stringify(state) })
        .then(() => { 
            document.getElementById('final-msg').innerHTML = "Данные успешно <b style='color:green'>сохранены в облаке</b>."; 
        })
        .catch(() => { 
            document.getElementById('final-msg').innerHTML = `
                <b style='color:red'>Ошибка отправки!</b> Пожалуйста, проверьте подключение к интернету.<br>
                <button class='btn btn-secondary' style='margin-top: 10px; margin-bottom: 10px; width: auto; padding: 8px 15px;' onclick='window.retryCloudSync()'>
                    ↻ Повторить отправку
                </button><br>
                <span style='font-size:0.9em; color:#555;'>Если ошибка сохраняется, разверните вкладку <b>«⚙️ Резервное сохранение»</b> чуть ниже и скачайте файл.</span>
            `; 
        });
    };
    // Запускаем первую попытку отправки
    window.retryCloudSync();
} else {
    console.log("DEV MODE: Отправка заблокирована.");
    document.getElementById('final-msg').innerHTML = "<b style='color:orange'>[РЕЖИМ РАЗРАБОТЧИКА]</b> Отправка в облако отключена.";
}
calculateAndShowResults();}

function toggleDetails(id) {
const el = document.getElementById(id);
if (!el) return;
const isOpening = (el.style.display === 'none' || el.style.display === '');
el.style.display = isOpening ? 'block' : 'none';
// Обновляем состояние кнопки
const button = document.querySelector(`[data-target="${id}"]`);
if (button) {
    button.setAttribute('aria-expanded', isOpening ? 'true' : 'false');
}
if (isOpening && id === 'detailsMilman') {
    renderMilmanDetailedCharts();
}
}
function renderMilmanDetailedCharts() {
if (!window.milmanData) {
    console.warn("Нет данных Мильмана для отрисовки");
    return;
}
const { scales_names, life_ideal_data, life_real_data, work_ideal_data, work_real_data } = window.milmanData;
// Уничтожаем старые графики, ТОЛЬКО если это Chart
if (window.chartMilmanLife && typeof window.chartMilmanLife.destroy === "function") {
    window.chartMilmanLife.destroy();
}
if (window.chartMilmanWork && typeof window.chartMilmanWork.destroy === "function") {
    window.chartMilmanWork.destroy();
}
// ЖИЗНЬ
const ctxLife = document.getElementById('chartMilmanLife');
if (ctxLife) {
    window.chartMilmanLife = new Chart(ctxLife.getContext('2d'), {
        type: 'line',
        data: {
            labels: scales_names,
            datasets: [
                {
                    label: 'Идеал',
                    data: life_ideal_data,
                    fill: true,
                    pointStyle: 'circle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                },
                {
                    label: 'Реальность',
                    data: life_real_data,
                    fill: true,
                    pointStyle: 'triangle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { min: 0 } }
        }
    });
}
// РАБОТА
const ctxWork = document.getElementById('chartMilmanWork');
if (ctxWork) {
    window.chartMilmanWork = new Chart(ctxWork.getContext('2d'), {
        type: 'line',
        data: {
            labels: scales_names,
            datasets: [
                {
                    label: 'Идеал',
                    data: work_ideal_data,
                    fill: true,
                    pointStyle: 'circle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                },
                {
                    label: 'Реальность',
                    data: work_real_data,
                    fill: true,
                    pointStyle: 'triangle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                }
            ]
        },
        options: { responsive: true, scales: { y: { min: 0 } }
        }
    });
}
// ===== ЭМОЦИОНАЛЬНЫЙ ПРОФИЛЬ (ПО МИЛЬМАНУ) =====
if (window.chartMilmanEmo && typeof window.chartMilmanEmo.destroy === "function") {
window.chartMilmanEmo.destroy();
}
const ctxEmo = document.getElementById("chartMilmanEmo");
if (ctxEmo) {
const labels = ["Обычное состояние", "Стрессовая ситуация"];
window.chartMilmanEmo = new Chart(ctxEmo.getContext("2d"), {
    type: "line",
    data: {
        labels,
        datasets: [
            {
                label: "Стенические реакции (активные)",
                data: [ emo.E_st, emo.F_st ],
                borderWidth: 3,
                tension: 0,
                fill: false,
                pointStyle: 'circle',
                pointRadius: 10,
                pointHoverRadius: 15
            },
            {
                label: "Астенические реакции (пассивные)",
                data: [ emo.E_ast, emo.F_ast ],
                borderWidth: 3,
                tension: 0,
                fill: false,
                pointStyle: 'circle',
                pointRadius: 10,
                pointHoverRadius: 15
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: true }
        },
        scales: {
            x: {
        offset: true,
    },
            y: {
                beginAtZero: true,
                suggestedMax: Math.max(
                    emo.E_ast, emo.E_st, emo.F_ast, emo.F_st
                ) + 3
            }
        }
        
    }
});
}
}
