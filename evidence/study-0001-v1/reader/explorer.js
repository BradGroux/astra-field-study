'use strict';
let data, selectedCell = null, spatial = null;
const $ = id => document.getElementById(id);
const fmt = n => Number(n).toLocaleString('en-US');
const short = n => n >= 1e9 ? (n / 1e9).toFixed(2) + 'B' : n >= 1e6 ? (n / 1e6).toFixed(2) + 'M' : fmt(n);
const sum = (rows, key) => rows.reduce((n, row) => n + row[key], 0);
const labels = { responses: 'Recorded responses', total_tokens: 'Recorded total tokens', corrective_units: 'Corrective contributions' };
const categoryLabels = [
  ['routine', 'Routine', '#788da8'], ['D_only', 'Dissatisfaction only', '#ee9da6'],
  ['C_only', 'Correction only', '#efb45c'], ['both', 'Both', '#b9a0f6'], ['ambiguous', 'Ambiguous', '#52647d'],
];

function selection() {
  return data.rows.filter(row => ($('day').value === 'all' || row.day === +$('day').value) &&
    ($('project').value === 'all' || row.project === $('project').value));
}

function metrics(element, items) {
  $(element).innerHTML = items.map(([value, label]) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`).join('');
}

function daily(rows) {
  const allDays = Array.from({ length: data.study_days }, (_, i) => i + 1);
  const maximum = Math.max(1, ...allDays.map(day => sum(data.rows.filter(row => row.day === day), 'responses')));
  $('daychart').innerHTML = '<div class="day-columns">' + allDays.map(day => {
    const value = sum(rows.filter(row => row.day === day), 'responses');
    const active = $('day').value === 'all' || day === +$('day').value;
    return `<div class="day-col ${value === maximum ? 'peak' : ''}"><strong>${active ? fmt(value) : '–'}</strong><i style="height:${value / maximum * 76}%"></i><span>Day ${day}</span></div>`;
  }).join('') + '</div>';
}

function ranking(rows) {
  const projects = [...new Set(data.rows.map(row => row.project))];
  const maximum = Math.max(1, ...projects.map(project => sum(data.rows.filter(row => row.project === project), 'responses')));
  const values = [...new Set(rows.map(row => row.project))].map(project => [project, sum(rows.filter(row => row.project === project), 'responses')]).sort((a, b) => b[1] - a[1]);
  $('projectchart').innerHTML = values.map(([project, value]) => `<div class="rank-row"><span>${project}</span><div class="rank-line" aria-hidden="true"><i style="left:${value / maximum * 100}%"></i></div><strong>${fmt(value)}</strong></div>`).join('');
}

function partition(rows) {
  const count = sum(rows, 'eligible');
  $('partition').innerHTML = '<div class="composition-strip" aria-hidden="true">' + categoryLabels.map(([key, , color]) => `<span style="width:${count ? sum(rows, key) / count * 100 : 0}%;background:${color}"></span>`).join('') + '</div><div class="partition-key">' + categoryLabels.map(([key, label, color]) => `<div style="--color:${color}"><span>${label}</span><strong>${sum(rows, key)}</strong><span>${count ? (100 * sum(rows, key) / count).toFixed(1) + '%' : 'Share unavailable'}</span></div>`).join('') + '</div>';
}

function updateProfile() {
  const rows = selection(), project = $('profileProject').value, key = $('metric').value;
  const maximum = Math.max(...data.rows.map(row => row[key]));
  $('profileTitle').textContent = `${project} · ${labels[key].toLowerCase()}`;
  $('profileScope').textContent = `This profile shows ${project} only. Height: 0 to ${fmt(maximum)}, fixed across projects. ${$('day').value === 'all' ? 'All six days are shown.' : 'Only Day ' + $('day').value + ' is included by the day filter.'}`;
  $('profileValues').innerHTML = Array.from({ length: data.study_days }, (_, index) => {
    const day = index + 1, row = rows.find(item => item.project === project && item.day === day);
    return `<button data-day="${day}" ${row ? '' : 'disabled'} aria-label="${project}, Day ${day}, ${row ? fmt(row[key]) + ' ' + labels[key].toLowerCase() : 'excluded by filter'}">Day ${day}<strong>${row ? short(row[key]) : 'Excluded'}</strong></button>`;
  }).join('');
  $('profileValues').querySelectorAll('button:not(:disabled)').forEach(button => button.addEventListener('click', () => detail(rows.find(row => row.project === project && row.day === +button.dataset.day))));
  if (spatial) spatial.update(rows, key, selectedCell, project);
}

function detail(row) {
  selectedCell = row;
  if ($('project').value === 'all') $('profileProject').value = row.project;
  $('cellDetail').textContent = `${row.project} · Day ${row.day}: ${fmt(row.responses)} recorded responses; ${fmt(row.total_tokens)} recorded total tokens; ${row.corrective_units} corrective contributions among ${row.eligible} substantive contributions${row.eligible ? ` (${(100 * row.corrective_units / row.eligible).toFixed(1)} per 100)` : ' (rate unavailable: no reviewed contributions)'}. Explicit dissatisfaction: ${row.dissatisfaction_units}; overlap: ${row.both}.`;
  updateProfile();
}

function matrix(rows) {
  const key = $('metric').value, maximum = Math.max(1, ...data.rows.map(row => row[key]));
  const days = [...new Set(rows.map(row => row.day))], projects = [...new Set(rows.map(row => row.project))];
  let table = '<table><thead><tr><th scope="col">Project</th>' + days.map(day => `<th scope="col">Day ${day}</th>`).join('') + '</tr></thead><tbody>';
  for (const project of projects) {
    table += `<tr><th scope="row">${project}</th>`;
    for (const day of days) {
      const row = rows.find(item => item.day === day && item.project === project), value = row[key], alpha = value / maximum;
      const rgb = [24, 41, 62].map((low, index) => Math.round(low + alpha * ([140, 186, 255][index] - low)));
      table += `<td><button style="background:rgb(${rgb.join(',')});color:${alpha > .45 ? '#0d1522' : '#eef3fa'}" data-day="${day}" data-project="${project}" aria-label="${project}, Day ${day}, ${fmt(value)} ${labels[key].toLowerCase()}">${short(value)}</button></td>`;
    }
    table += '</tr>';
  }
  $('matrix').innerHTML = table + '</tbody></table>';
  $('matrix').querySelectorAll('button').forEach(button => button.addEventListener('click', () => detail(rows.find(row => row.day === +button.dataset.day && row.project === button.dataset.project))));
}

function render() {
  const rows = selection(), n = sum(rows, 'eligible'), c = sum(rows, 'corrective_units');
  const d = sum(rows, 'dissatisfaction_units'), both = sum(rows, 'both');
  const input = sum(rows, 'input_tokens'), cache = sum(rows, 'cached_input_tokens');
  $('scope').textContent = `${$('day').value === 'all' ? 'All six days' : 'Day ' + $('day').value} · ${$('project').value === 'all' ? 'All projects' : $('project').value}`;
  metrics('metrics', [[fmt(sum(rows, 'responses')), 'Recorded responses'], [short(sum(rows, 'total_tokens')), 'Recorded total tokens'], [input ? (100 * cache / input).toFixed(2) + '%' : 'Unavailable', 'Cached share of input tokens']]);
  daily(rows); ranking(rows); partition(rows);
  metrics('codedmetrics', [[fmt(n), 'Substantive contributions'], [fmt(c), 'Corrective contributions'], [n ? (100 * c / n).toFixed(2) : 'Unavailable', 'Corrective contributions per 100 reviewed']]);
  $('codingnote').textContent = `${d} contributions express dissatisfaction; ${c} contain corrective steering; ${both} contain both. The five exclusive categories total ${n}. ${n ? 'These proportions describe the reviewed contributions.' : 'No contributions were reviewed for this selection; a rate is unavailable.'}`;
  $('metricnote').textContent = `${labels[$('metric').value]} · Linear color scale: 0 to ${fmt(Math.max(...data.rows.map(row => row[$('metric').value])))}, fixed across selections. ` + ($('metric').value === 'corrective_units' ? 'Select a cell to see its contribution denominator.' : $('metric').value === 'total_tokens' ? 'Includes cached and repeated context.' : 'Each cell reports retained response activity.');
  matrix(rows);
  const repository = data.repository.filter(row => $('project').value === 'all' || row.project === $('project').value);
  $('repo').innerHTML = repository.length ? '<div class="table-wrap"><table><thead><tr><th scope="col">Project</th><th scope="col">Active issues</th><th scope="col">PRs merged</th><th scope="col">Net changed paths</th></tr></thead><tbody>' + repository.map(row => `<tr><th scope="row">${row.project}</th><td>${fmt(row.issues)}</td><td>${fmt(row.merged)}</td><td>${fmt(row.paths)}</td></tr>`).join('') + `<tr><th scope="row">Selected projects · full window</th><td>${fmt(sum(repository, 'issues'))}</td><td>${fmt(sum(repository, 'merged'))}</td><td>${fmt(sum(repository, 'paths'))}</td></tr></tbody></table></div>` : '<p>No repository-history data for this project. The identity was unresolved; this is missing data, not zero activity.</p>';
  if (selectedCell && !rows.some(row => row.day === selectedCell.day && row.project === selectedCell.project)) {
    selectedCell = null; $('cellDetail').textContent = 'Select a cell to inspect its exact counts and denominator.';
  }
  $('profileProject').disabled = $('project').value !== 'all';
  if ($('project').value !== 'all') $('profileProject').value = $('project').value;
  updateProfile();
}

fetch('explorer-data.json').then(response => {
  if (!response.ok) throw Error('Data unavailable');
  return response.json();
}).then(result => {
  data = result;
  for (let day = 1; day <= data.study_days; day++) $('day').add(new Option('Day ' + day, day));
  for (const project of [...new Set(data.rows.map(row => row.project))]) {
    $('project').add(new Option(project, project)); $('profileProject').add(new Option(project, project));
  }
  $('profileProject').value = [...new Set(data.rows.map(row => row.project))].sort((a, b) => sum(data.rows.filter(row => row.project === b), 'responses') - sum(data.rows.filter(row => row.project === a), 'responses'))[0];
  $('profileProject').onchange = updateProfile;
  for (const id of ['day', 'project', 'metric']) $(id).addEventListener('change', render);
  $('reset').onclick = () => { $('day').value = 'all'; $('project').value = 'all'; render(); };
  $('download').onclick = () => {
    const output = { format: 'observational_evidence_selection', format_version: '1.0', synthetic: data.synthetic, study_days: data.study_days, scope: $('scope').textContent, definitions: data.definitions, rows: selection(), repository_scope: 'Always full six-day window; project filter only', repository: data.repository.filter(row => $('project').value === 'all' || row.project === $('project').value) };
    const url = URL.createObjectURL(new Blob([JSON.stringify(output, null, 2)], { type: 'application/json' }));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'astra-selected-aggregates.json'; anchor.click(); URL.revokeObjectURL(url);
  };
  $('view3d').onclick = async () => {
    const open = $('spatial').hidden;
    $('spatial').hidden = !open; $('view3d').setAttribute('aria-pressed', String(open));
    $('view3d').textContent = open ? 'Close 3D project profile' : 'Open 3D project profile';
    if (open && !spatial) {
      try {
        const module = await import('./spatial.js');
        spatial = await module.createSpatial($('scene'), data, detail);
        $('webglstatus').textContent = 'Choose a project or select a day below for exact values. Camera movement is controlled by the sliders.';
        for (const id of ['angle', 'elevation']) $(id).oninput = () => spatial.camera(+$('angle').value, +$('elevation').value);
        $('cameraReset').onclick = () => { $('angle').value = 12; $('elevation').value = 18; spatial.camera(12, 18); };
      } catch (error) {
        $('webglstatus').textContent = '3D is unavailable in this browser. Exact project values, filters and the matrix remain available.';
      }
    }
    if (open) updateProfile();
  };
  render();
}).catch(() => { $('scope').textContent = 'Data could not load. Open through the local preview server. The article figures remain available.'; });
