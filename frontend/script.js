const BACKEND_URL = 'http://127.0.0.1:7860';
let currentTimetableData = null;

const SUBJECT_COLORS = [
    '#FFE5E5', '#E5F5FF', '#E5FFE5', '#FFF5E5', '#FFE5FF',
    '#E5FFFF', '#FFFFE5', '#FFE5F5', '#F5E5FF', '#F5FFE5'
];

document.addEventListener('DOMContentLoaded', () => {
    loadExample();
});

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    }[character]));
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(showToast.timeout);
    showToast.timeout = setTimeout(() => toast.classList.remove('visible'), 4200);
}

function addSubjectRow(subject = '', teacher = '', hours = '') {
    const container = document.getElementById('subjects-container');
    const row = document.createElement('div');
    row.className = 'subject-row';
    row.innerHTML = `
        <input type="text" aria-label="Subject" placeholder="e.g. Mathematics" value="${escapeHtml(subject)}" class="subject-name">
        <input type="text" aria-label="Teacher" placeholder="e.g. Dr. Smith" value="${escapeHtml(teacher)}" class="teacher-name">
        <input type="number" aria-label="Hours per week" placeholder="Hours" value="${escapeHtml(hours)}" min="1" max="10" class="subject-hours">
        <button type="button" class="btn-remove" onclick="this.parentElement.remove()">✕</button>
    `;
    container.appendChild(row);
}

function addRoomRow(roomId = '', capacity = '') {
    const container = document.getElementById('rooms-container');
    const row = document.createElement('div');
    row.className = 'room-row';
    row.innerHTML = `
        <input type="text" aria-label="Room ID" placeholder="e.g. R101" value="${escapeHtml(roomId)}" class="room-id">
        <input type="number" aria-label="Room capacity" placeholder="Capacity" value="${escapeHtml(capacity)}" min="1" max="100" class="room-capacity">
        <button type="button" class="btn-remove" onclick="this.parentElement.remove()">✕</button>
    `;
    container.appendChild(row);
}

function loadExample() {
    document.getElementById('subjects-container').innerHTML = '';
    document.getElementById('rooms-container').innerHTML = '';
    
    document.getElementById('days').value = 'Monday,Tuesday,Wednesday,Thursday,Friday';
    document.getElementById('periods').value = '6';
    
    addSubjectRow('Mathematics', 'Dr. Smith', '5');
    addSubjectRow('English', 'Ms. Johnson', '4');
    addSubjectRow('Physics', 'Dr. Brown', '3');
    addSubjectRow('History', 'Mr. Davis', '3');
    addSubjectRow('Chemistry', 'Dr. Wilson', '3');
    addSubjectRow('Biology', 'Ms. Taylor', '3');
    addSubjectRow('PE', 'Mr. Anderson', '2');
    addSubjectRow('Art', 'Ms. Martinez', '2');
    
    addRoomRow('R101', '30');
    addRoomRow('R102', '25');
    addRoomRow('Lab1', '20');
    addRoomRow('Gym', '40');
}

function collectFormData() {
    const days = document.getElementById('days').value.split(',').map(d => d.trim());
    const periodsPerDay = parseInt(document.getElementById('periods').value, 10);
    
    const subjectRows = document.querySelectorAll('.subject-row');
    const teachers = new Map();
    const classes = [];
    
    subjectRows.forEach((row, index) => {
        const subjectName = row.querySelector('.subject-name').value.trim();
        const teacherName = row.querySelector('.teacher-name').value.trim();
        const hours = parseInt(row.querySelector('.subject-hours').value, 10);
        
        if (subjectName || teacherName || Number.isFinite(hours)) {
            if (!subjectName || !teacherName || !Number.isInteger(hours) || hours < 1) {
                throw new Error('Each subject needs a name, teacher, and positive hours');
            }
            const teacherId = `T${teachers.size + 1}`;
            if (!teachers.has(teacherName)) {
                teachers.set(teacherName, teacherId);
            }
            
            classes.push({
                id: `C${index + 1}`,
                subject: subjectName,
                teacher_id: teachers.get(teacherName),
                hours_per_week: hours
            });
        }
    });
    
    const roomRows = document.querySelectorAll('.room-row');
    const rooms = [];
    
    roomRows.forEach(row => {
        const roomId = row.querySelector('.room-id').value.trim();
        const capacity = parseInt(row.querySelector('.room-capacity').value, 10);
        
        if (roomId || Number.isFinite(capacity)) {
            if (!roomId || !Number.isInteger(capacity) || capacity < 1) {
                throw new Error('Each room needs an ID and positive capacity');
            }
            rooms.push({ id: roomId, capacity: capacity });
        }
    });
    
    const teachersArray = Array.from(teachers.entries()).map(([name, id]) => ({
        id: id,
        name: name
    }));
    
    if (days.length === 0 || days.some(day => !day)) throw new Error('Please enter at least one valid day');
    if (!Number.isInteger(periodsPerDay) || periodsPerDay < 1) throw new Error('Periods per day must be positive');
    if (classes.length === 0) throw new Error('Please add at least one subject');
    if (rooms.length === 0) throw new Error('Please add at least one room');
    
    return {
        days: days,
        periods_per_day: periodsPerDay,
        rooms: rooms,
        teachers: teachersArray,
        classes: classes
    };
}

async function generateTimetable() {
    try {
        const formData = collectFormData();
        const popSize = parseInt(document.getElementById('popSize').value);
        const generations = parseInt(document.getElementById('generations').value);
        const seedInput = document.getElementById('seed').value;
        const seed = seedInput ? parseInt(seedInput) : Math.floor(Math.random() * 10000);
        
        document.getElementById('loadingOverlay').style.display = 'grid';
        document.getElementById('outputSection').style.display = 'none';
        
        const jsonInput = JSON.stringify(formData);
        
        const response = await fetch(`${BACKEND_URL}/gradio_api/call/generate_timetable_json`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: [jsonInput, popSize, generations, seed] })
        });
        
        if (!response.ok) {
            throw new Error(`Backend returned status ${response.status}`);
        }
        
        const result = await response.json();
        const eventId = result.event_id;
        const finalResult = await pollForResult(eventId);
        
        document.getElementById('loadingOverlay').style.display = 'none';
        displayResults(finalResult);
        
    } catch (error) {
        document.getElementById('loadingOverlay').style.display = 'none';
        showError(error.message);
    }
}

async function pollForResult(eventId) {
    return new Promise((resolve, reject) => {
        const eventSource = new EventSource(`${BACKEND_URL}/gradio_api/call/generate_timetable_json/${eventId}`);
        
        eventSource.addEventListener('complete', (event) => {
            eventSource.close();
            const data = JSON.parse(event.data);
            resolve(data);
        });
        
        eventSource.addEventListener('error', () => {
            eventSource.close();
            reject(new Error('Failed to get result from backend'));
        });
        
        setTimeout(() => {
            eventSource.close();
            reject(new Error('Request timed out'));
        }, 60000);
    });
}

function displayResults(result) {
    const [htmlTable, plot, warning, downloadJson] = result;
    
    if (!downloadJson) {
        showError('No data returned from backend');
        return;
    }
    
    try {
        currentTimetableData = JSON.parse(downloadJson);
        if (currentTimetableData.error) {
            showError(currentTimetableData.error);
            return;
        }
        
        document.getElementById('outputSection').style.display = 'block';
        
        const statusDiv = document.getElementById('statusMessage');
        statusDiv.innerHTML = currentTimetableData.final_fitness === 0
            ? '<div class="status-success">✓ Perfect schedule generated with no conflicts</div>'
            : `<div class="status-warning">⚠ ${Math.abs(currentTimetableData.final_fitness)} penalty points remain. You can try more generations.</div>`;
        
        const fitnessDiv = document.getElementById('fitnessInfo');
        fitnessDiv.innerHTML = `
            <div class="metric"><div class="metric-label">FINAL FITNESS</div><div class="metric-value ${currentTimetableData.final_fitness === 0 ? 'good' : 'warn'}">${currentTimetableData.final_fitness}</div></div>
            <div class="metric"><div class="metric-label">GENERATIONS RUN</div><div class="metric-value">${currentTimetableData.generations_run}</div></div>
            <div class="metric"><div class="metric-label">SCHEDULE STATUS</div><div class="metric-value ${currentTimetableData.final_fitness === 0 ? 'good' : 'warn'}">${currentTimetableData.final_fitness === 0 ? 'Ready' : 'Review'}</div></div>
        `;
        
        renderTimetable(currentTimetableData.timetable);
        renderFitnessChart(currentTimetableData.best_fitness_history);
        
        document.getElementById('outputSection').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        showError('Error parsing results: ' + error.message);
    }
}

function renderTimetable(timetable) {
    const container = document.getElementById('timetableContainer');
    
    if (!timetable || timetable.length === 0) {
        container.innerHTML = '<p>No timetable data</p>';
        return;
    }
    
    const subjects = new Set();
    timetable.forEach(day => {
        day.periods.forEach(period => {
            period.classes.forEach(classItem => subjects.add(classItem.subject));
        });
    });
    
    const subjectColorMap = {};
    Array.from(subjects).forEach((subject, index) => {
        subjectColorMap[subject] = SUBJECT_COLORS[index % SUBJECT_COLORS.length];
    });
    
    let html = '<table class="timetable">';
    html += '<tr><th>Period</th>';
    timetable.forEach(day => {
        html += `<th>${day.day}</th>`;
    });
    html += '</tr>';
    
    const numPeriods = timetable[0].periods.length;
    for (let p = 0; p < numPeriods; p++) {
        html += `<tr><th>Period ${p + 1}</th>`;
        
        timetable.forEach(day => {
            const period = day.periods[p];
            
            if (!period.classes || period.classes.length === 0) {
                html += '<td class="free">Free</td>';
            } else {
                html += '<td>';
                period.classes.forEach(classItem => {
                    const bgColor = subjectColorMap[classItem.subject];
                    html += `<div class="schedule-item" style="background-color: ${bgColor};">`;
                    html += `<strong>${escapeHtml(classItem.subject)}</strong>`;
                    html += `<span>${escapeHtml(classItem.teacher)} · ${escapeHtml(classItem.room)}</span>`;
                    html += '</div>';
                });
                html += '</td>';
            }
        });
        
        html += '</tr>';
    }
    
    html += '</table>';
    container.innerHTML = html;
}

function renderFitnessChart(history) {
    const canvas = document.getElementById('fitnessChart');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;
    
    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    
    ctx.clearRect(0, 0, width, height);
    
    if (!history || history.length === 0) return;
    
    const minFitness = Math.min(...history);
    const maxFitness = Math.max(...history);
    const range = maxFitness - minFitness || 1;
    
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    ctx.strokeStyle = '#0066cc';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    history.forEach((fitness, index) => {
        const x = padding + (width - 2 * padding) * index / (history.length - 1 || 1);
        const y = height - padding - (height - 2 * padding) * (fitness - minFitness) / range;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    ctx.fillStyle = '#333';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Generation', width / 2, height - 5);
    
    ctx.save();
    ctx.translate(15, height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Fitness', 0, 0);
    ctx.restore();
}

function downloadJSON() {
    if (!currentTimetableData) {
        alert('No timetable data to download');
        return;
    }
    
    const dataStr = JSON.stringify(currentTimetableData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'timetable.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function showError(message) {
    document.getElementById('outputSection').style.display = 'block';
    
    let errorMessage = message;
    
    if (message.includes('Failed to fetch') || message.includes('NetworkError') || message.includes('refused')) {
        errorMessage = `
            <strong>Cannot connect to backend!</strong><br><br>
            Make sure the backend is running:<br>
            <code>python app.py</code><br><br>
            Then wait for: "Running on local URL: http://127.0.0.1:7860"
        `;
    }
    
    document.getElementById('statusMessage').innerHTML = `<div class="status-error">× ${errorMessage}</div>`;
    document.getElementById('fitnessInfo').innerHTML = '';
    document.getElementById('timetableContainer').innerHTML = '';
    
    const canvas = document.getElementById('fitnessChart');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    document.getElementById('outputSection').scrollIntoView({ behavior: 'smooth' });
    showToast(message);
}
