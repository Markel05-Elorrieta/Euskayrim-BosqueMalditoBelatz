// ==================== Variables ====================
let selectedHeroes = [];
let heroesData = [];
const MAX_HEROES = 4;
const MAX_POINTS = 5;
let heroBonusPoints = {};

// ==================== Al cargar DOM ====================
document.addEventListener('DOMContentLoaded', () => {
    initializePage();
});

// ==================== Inicialización ====================
function initializePage() {
    loadHeroes();
    checkApiStatus();
    renderHeroBonusPanels();

    document.getElementById('whatif-form')?.addEventListener('submit', handleWhatIfSubmit);
    document.getElementById('divine-btn')?.addEventListener('click', handleDivineCall);
    document.getElementById('check-api-btn')?.addEventListener('click', checkApiStatus);

    // Botones de dificultad para What-If
    document.querySelectorAll('#dificultad-group .difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#dificultad-group .difficulty-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Botones de dificultad para Divine-Call
    document.querySelectorAll('#divine-dificultad-group .difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#divine-dificultad-group .difficulty-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
    document.getElementById('reload-heroes-btn')?.addEventListener('click', () => {
        selectedHeroes = [];
        heroBonusPoints = {};
        loadHeroes();
        renderHeroBonusPanels();
    });
}

// ==================== Cargar héroes ====================
async function loadHeroes() {
    try {
        const response = await fetch('/heroes');
        if (!response.ok) throw new Error('Error al cargar héroes');

        heroesData = await response.json();
        renderHeroes(heroesData);
    } catch (error) {
        console.error('Error:', error);
        showError('No se pudieron cargar los héroes');
    }
}

function renderHeroes(heroes) {
    const grid = document.getElementById('heroes-grid');
    grid.innerHTML = '';

    heroes.forEach(hero => {
        const heroCard = document.createElement('div');
        heroCard.className = 'hero-card';
        heroCard.dataset.heroId = hero.id;
        heroCard.innerHTML = `
            <div class="hero-name">${hero.nombre}</div>
            <div class="hero-stats">
                Vida: ${hero.vida}<br>
                Mana: ${hero.mana}<br>
                Físico: ${hero.fisico}<br>
                Agilidad: ${hero.agilidad}
            </div>
        `;

        heroCard.addEventListener('click', () => toggleHeroSelection(heroCard, hero));
        grid.appendChild(heroCard);
    });
}

function toggleHeroSelection(card, hero) {
    const isSelected = card.classList.contains('selected');

    if (isSelected) {
        card.classList.remove('selected');
        selectedHeroes = selectedHeroes.filter(h => h.id !== hero.id);
        delete heroBonusPoints[hero.id];
    } else {
        if (selectedHeroes.length >= MAX_HEROES) {
            showError('Ya has seleccionado 4 héroes');
            return;
        }
        card.classList.add('selected');
        selectedHeroes.push(hero);
        heroBonusPoints[hero.id] = { vida: 0, mana: 0, fisico: 0, agilidad: 0 };
    }

    renderHeroBonusPanels();
    updateHeroError();
}

function updateHeroError() {
    const errorDiv = document.getElementById('hero-error');
    if (selectedHeroes.length !== MAX_HEROES) {
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }
}

// ==================== Paneles de puntos por héroe ====================
function renderHeroBonusPanels() {
    const container = document.getElementById('hero-points-container');
    container.innerHTML = '';

    if (selectedHeroes.length === 0) {
        container.innerHTML = '<p class="helper-text" style="text-align:center; opacity:0.5;">Selecciona héroes para distribuir sus puntos</p>';
        return;
    }

    selectedHeroes.forEach(hero => {
        const bonus = heroBonusPoints[hero.id] || { vida: 0, mana: 0, fisico: 0, agilidad: 0 };
        const totalUsed = bonus.vida + bonus.mana + bonus.fisico + bonus.agilidad;
        const remaining = MAX_POINTS - totalUsed;

        const panel = document.createElement('div');
        panel.className = 'hero-bonus-panel';
        panel.dataset.heroId = hero.id;
        panel.innerHTML = `
            <div class="hero-bonus-header">
                <span class="hero-bonus-name">${hero.nombre}</span>
                <span class="hero-bonus-remaining ${remaining === 0 ? 'complete' : remaining < 0 ? 'exceeded' : ''}">
                    Restantes: <strong>${remaining}</strong> / ${MAX_POINTS}
                </span>
            </div>
            <div class="hero-bonus-stats">
                ${renderStatSlider(hero, 'vida', bonus.vida)}
                ${renderStatSlider(hero, 'mana', bonus.mana)}
                ${renderStatSlider(hero, 'fisico', bonus.fisico)}
                ${renderStatSlider(hero, 'agilidad', bonus.agilidad)}
            </div>
            <div class="hero-bonus-total">
                Total atributos: <strong>${hero.vida + hero.mana + hero.fisico + hero.agilidad + totalUsed}</strong> / 20
            </div>
        `;

        container.appendChild(panel);
    });

    // Añadir event listeners a los sliders
    container.querySelectorAll('.hero-stat-slider').forEach(slider => {
        slider.addEventListener('input', handleSliderChange);
    });
}

function renderStatSlider(hero, stat, bonusValue) {
    const statLabels = { vida: 'Vida', mana: 'Mana', fisico: 'Físico', agilidad: 'Agilidad' };
    const baseValue = hero[stat];
    return `
        <div class="hero-stat-row">
            <label class="hero-stat-label">
                ${statLabels[stat]}: <span class="hero-stat-base">${baseValue}</span> + <span class="hero-stat-bonus">${bonusValue}</span> = <strong>${baseValue + bonusValue}</strong>
            </label>
            <input type="range" class="hero-stat-slider stat-input-field"
                   data-hero-id="${hero.id}"
                   data-stat="${stat}"
                   min="0" max="${MAX_POINTS}" value="${bonusValue}">
        </div>
    `;
}

function handleSliderChange(e) {
    const slider = e.target;
    const heroId = parseInt(slider.dataset.heroId);
    const stat = slider.dataset.stat;
    let newValue = parseInt(slider.value) || 0;

    const bonus = heroBonusPoints[heroId];
    if (!bonus) return;

    // Calcular total sin el stat actual
    const otherTotal = Object.keys(bonus)
        .filter(k => k !== stat)
        .reduce((sum, k) => sum + bonus[k], 0);

    // Limitar si excede MAX_POINTS
    if (otherTotal + newValue > MAX_POINTS) {
        newValue = MAX_POINTS - otherTotal;
        slider.value = newValue;
    }

    bonus[stat] = newValue;
    heroBonusPoints[heroId] = bonus;

    updatePanelLabels(heroId);
    validateAllPoints();
}

function updatePanelLabels(heroId) {
    const panel = document.querySelector(`.hero-bonus-panel[data-hero-id="${heroId}"]`);
    if (!panel) return;

    const hero = selectedHeroes.find(h => h.id === heroId);
    if (!hero) return;

    const bonus = heroBonusPoints[heroId];
    const totalUsed = bonus.vida + bonus.mana + bonus.fisico + bonus.agilidad;
    const remaining = MAX_POINTS - totalUsed;

    // Actualizar contador de puntos restantes
    const remainingSpan = panel.querySelector('.hero-bonus-remaining');
    remainingSpan.innerHTML = `Restantes: <strong>${remaining}</strong> / ${MAX_POINTS}`;
    remainingSpan.className = 'hero-bonus-remaining ' + (remaining === 0 ? 'complete' : remaining < 0 ? 'exceeded' : '');

    // Actualizar cada stat
    ['vida', 'mana', 'fisico', 'agilidad'].forEach(stat => {
        const row = panel.querySelector(`input[data-stat="${stat}"]`).closest('.hero-stat-row');
        const bonusSpan = row.querySelector('.hero-stat-bonus');
        const strongEl = row.querySelector('strong');
        bonusSpan.textContent = bonus[stat];
        strongEl.textContent = hero[stat] + bonus[stat];
    });

    // Actualizar total de atributos
    const totalDiv = panel.querySelector('.hero-bonus-total');
    totalDiv.innerHTML = `Total atributos: <strong>${hero.vida + hero.mana + hero.fisico + hero.agilidad + totalUsed}</strong> / 20`;
}

function validateAllPoints() {
    const errorDiv = document.getElementById('points-error');
    let allValid = true;

    for (const hero of selectedHeroes) {
        const bonus = heroBonusPoints[hero.id];
        const total = bonus.vida + bonus.mana + bonus.fisico + bonus.agilidad;
        if (total !== MAX_POINTS) {
            allValid = false;
            break;
        }
    }

    if (!allValid && selectedHeroes.length > 0) {
        errorDiv.textContent = '⚠️ Cada héroe debe tener exactamente 5 puntos de Bendición distribuidos';
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }

    return allValid;
}

// ==================== What-If ====================
async function handleWhatIfSubmit(e) {
    e.preventDefault();

    // Validar exactamente 4 héroes seleccionados
    if (selectedHeroes.length !== MAX_HEROES) {
        showError('Selecciona exactamente 4 héroes');
        return;
    }

    // Validar distribución de puntos
    if (!validateAllPoints()) {
        showError('Distribuye exactamente los 5 puntos de Bendición en cada héroe');
        return;
    }

    const data = {
        dificultad: parseFloat(document.querySelector('#dificultad-group .difficulty-btn.active').dataset.value)
    };

    const allHeroKeys = heroesData.map(hero => 
        hero.nombre.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    );

    // Inicializar todos a 0
    allHeroKeys.forEach(key => {
        data[`${key}_en_equipo`] = 0;
        data[`${key}_vida`] = 0;
        data[`${key}_mana`] = 0;
        data[`${key}_fisico`] = 0;
        data[`${key}_agilidad`] = 0;
    });

    // Rellenar los héroes seleccionados con base + bonus
    selectedHeroes.forEach(hero => {
        const key = hero.nombre.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const bonus = heroBonusPoints[hero.id];

        data[`${key}_en_equipo`] = 1;
        data[`${key}_vida`] = hero.vida + bonus.vida;
        data[`${key}_mana`] = hero.mana + bonus.mana;
        data[`${key}_fisico`] = hero.fisico + bonus.fisico;
        data[`${key}_agilidad`] = hero.agilidad + bonus.agilidad;
    });

    try {
        const response = await fetch('/what-if', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en la predicción');
        }

        const result = await response.json();
        showResult(result);
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

function showResult(result) {
    const container = document.getElementById('result-container');
    container.style.display = 'block';

    document.getElementById('probabilidad').textContent = (result.probabilidad_exito * 100).toFixed(2) + '%';

    const probValue = result.probabilidad_exito;
    const probElement = document.getElementById('probabilidad');

    // Recomendación basada en la probabilidad
    let recomendacion, recoClass;
    if (probValue > 0.7) {
        recomendacion = 'Adelante, la gloria os espera!';
        recoClass = 'success';
    } else if (probValue > 0.5) {
        recomendacion = 'Las posibilidades están a vuestro favor!';
        recoClass = 'success';
    } else if (probValue > 0.4) {
        recomendacion = 'Resultado incierto, reforzad el equipo!';
        recoClass = 'warning';
    } else {
        recomendacion = 'Peligro extremo, hay que replantear la estrategia!';
        recoClass = 'danger';
    }
    const recoEl = document.getElementById('recomendacion');
    recoEl.textContent = recomendacion;
    recoEl.className = 'result-value ' + recoClass;

    // Predicción
    const prediccionEl = document.getElementById('prediccion');
    const esVictoria = result.prediccion === 'Victoria';
    prediccionEl.textContent = esVictoria ? '⚔️ Victoria' : '💀 Derrota';
    prediccionEl.className = 'result-value ' + (esVictoria ? 'success' : 'danger');

    if (probValue > 0.7) {
        probElement.className = 'result-value success';
    } else if (probValue > 0.4) {
        probElement.className = 'result-value warning';
    } else {
        probElement.className = 'result-value danger';
    }

    const fill = document.querySelector('.result-visual-fill');
    const marker = document.querySelector('.result-visual-marker');
    if (fill) {
        fill.className = 'result-visual-fill ' + (probValue > 0.7 ? 'success' : probValue > 0.4 ? 'warning' : 'danger');
        setTimeout(() => {
            fill.style.width = `${probValue * 100}%`;
        }, 100);
    }
    if (marker) {
        setTimeout(() => {
            marker.style.left = `${probValue * 100}%`;
        }, 100);
    }

    // Smooth scroll to result
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 200);
}

// ==================== Llamada divina ====================

async function handleDivineCall() {
    const activeBtn = document.querySelector('#divine-dificultad-group .difficulty-btn.active');
    const dificultad = activeBtn ? parseInt(activeBtn.dataset.value) : 1;

    document.getElementById('divine-loading').style.display = 'block';
    document.getElementById('divine-result').style.display = 'none';
    document.getElementById('divine-btn').disabled = true;

    try {
        const response = await fetch('/divine-call', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dificultad })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en Divine-Call');
        }

        const result = await response.json();
        showDivineResult(result);
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        document.getElementById('divine-loading').style.display = 'none';
        document.getElementById('divine-btn').disabled = false;
    }
}

function showDivineResult(result) {
    const container = document.getElementById('divine-result');
    const details = document.getElementById('best-team-details');
    const combosDiv = document.getElementById('divine-all-combos');

    const bestProb = result.probabilidad_maxima;
    const probClass = bestProb > 0.7 ? 'success' : bestProb > 0.4 ? 'warning' : 'danger';
    const blessingHtml = formatDivineBlessing(result.bendicion_optima);

    details.innerHTML = `
        <div class="result-item">
            <span class="result-label"><i class="bi bi-percent"></i> Probabilidad máxima</span>
            <span class="result-value ${probClass}">${(bestProb * 100).toFixed(2)}%</span>
        </div>
        <div class="result-item">
            <span class="result-label"><i class="bi bi-people-fill"></i> Mejor equipo</span>
            <span class="result-value">${result.heroes.join(', ')}</span>
        </div>
        <div class="result-item">
            <span class="result-label"><i class="bi bi-trophy-fill"></i> Predicción</span>
            <span class="result-value ${result.prediccion === 'Victoria' ? 'success' : 'danger'}">
                ${result.prediccion === 'Victoria' ? '⚔️ Victoria' : '💀 Derrota'}
            </span>
        </div>
        <div class="result-item">
            <span class="result-label"><i class="bi bi-magic"></i> Bendición óptima</span>
            <span class="result-value">${blessingHtml}</span>
        </div>
    `;

    if (result.todas_combinaciones && result.todas_combinaciones.length > 0) {
        let combosHTML = '<h4><i class="bi bi-list-ol"></i> Ranking de todas las combinaciones</h4>';
        result.todas_combinaciones.forEach((combo, idx) => {
            const p = combo.probabilidad_exito;
            const pClass = p > 0.7 ? 'success' : p > 0.4 ? 'warning' : 'danger';
            const isBest = idx === 0 ? ' best' : '';
            combosHTML += `
                <div class="divine-combo-item${isBest}">
                    <span class="divine-combo-rank">#${idx + 1}</span>
                    <span class="divine-combo-heroes">${combo.heroes.join(', ')}</span>
                    <span class="divine-combo-prob ${pClass}">${(p * 100).toFixed(2)}%</span>
                </div>
            `;
        });
        combosDiv.innerHTML = combosHTML;
    } else {
        combosDiv.innerHTML = '';
    }

    container.style.display = 'block';

    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 200);
}

// ==================== API Status ====================
async function checkApiStatus() {
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const modelDot = document.getElementById('model-dot');
    const modelText = document.getElementById('model-text');

    try {
        const response = await fetch('/health');
        if (response.ok) {
            const data = await response.json();

            statusDot.className = 'status-indicator online';
            statusText.textContent = 'API en línea y funcionando';
            statusText.style.color = 'var(--success-color)';

            if (data.modelo_cargado) {
                modelDot.className = 'status-indicator online';
                modelText.textContent = 'Modelo de predicción cargado correctamente';
                modelText.style.color = 'var(--success-color)';
            } else {
                modelDot.className = 'status-indicator';
                modelText.textContent = 'Modelo de predicción NO cargado';
                modelText.style.color = 'var(--danger-color)';
            }
        } else {
            statusDot.className = 'status-indicator';
            statusText.textContent = 'API no responde correctamente';
            statusText.style.color = 'var(--danger-color)';
            modelDot.className = 'status-indicator';
            modelText.textContent = 'No se pudo verificar el modelo de predicción';
            modelText.style.color = 'var(--warning-color)';
        }
    } catch (error) {
        statusDot.className = 'status-indicator';
        statusText.textContent = 'API no accesible';
        statusText.style.color = 'var(--danger-color)';
        modelDot.className = 'status-indicator';
        modelText.textContent = 'No se pudo verificar el modelo de predicción';
        modelText.style.color = 'var(--warning-color)';
    }
}

// ==================== Utilidades ====================
function showError(message) {
    alert('⚠️ ' + message);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializePage,
        loadHeroes,
        handleWhatIfSubmit,
        checkApiStatus
    };
}

function formatDivineBlessing(bendicionOptima) {
    if (!bendicionOptima || typeof bendicionOptima !== 'object') {
        return 'No disponible';
    }

    return Object.entries(bendicionOptima)
        .map(([hero, bonus]) => {
            const vida = bonus?.vida ?? 0;
            const mana = bonus?.mana ?? 0;
            const fisico = bonus?.fisico ?? 0;
            const agilidad = bonus?.agilidad ?? 0;
            return `${hero}: Vida +${vida}, Mana +${mana}, Físico +${fisico}, Agilidad +${agilidad}`;
        })
        .join('<br>');
}