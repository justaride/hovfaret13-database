const DATA_URL = 'data/solstudie.json';

const dom = {
  seriesContainer: document.getElementById('series-buttons'),
  frameVideo: document.getElementById('frame-video'),
  frameImage: document.getElementById('frame-image'),
  frameLabel: document.getElementById('frame-label'),
  frameIndex: document.getElementById('frame-index'),
  frameTime: document.getElementById('frame-time'),
  frameSlider: document.getElementById('frame-slider'),
  playToggle: document.getElementById('play-toggle'),
  prevButton: document.getElementById('prev-frame'),
  nextButton: document.getElementById('next-frame'),
  speedInput: document.getElementById('speed-input'),
  speedValue: document.getElementById('speed-value'),
  loopToggle: document.getElementById('loop-toggle'),
  brightnessInput: document.getElementById('brightness-input'),
  contrastInput: document.getElementById('contrast-input'),
  viewerFrame: document.getElementById('viewer-frame'),
  viewerEmpty: document.getElementById('viewer-empty'),
  statFrames: document.getElementById('stat-frames'),
  statSeries: document.getElementById('stat-series'),
  statFps: document.getElementById('stat-fps'),
  overlayGrid: document.querySelector('[data-overlay="grid"]'),
  overlaySunpath: document.querySelector('[data-overlay="sunpath"]'),
  overlayShadow: document.querySelector('[data-overlay="shadow"]'),
};

let data = null;
let state = {
  seriesId: null,
  frameIndex: 0,
  fps: 1,
  mode: 'frames',
  playing: false,
  loop: true,
  timer: null,
};

function setPlaybackStatus(isPlaying) {
  state.playing = isPlaying;
  dom.playToggle.textContent = isPlaying ? 'Pause' : 'Spill';
  dom.playToggle.classList.toggle('btn-secondary', isPlaying);
  dom.playToggle.classList.toggle('btn-primary', !isPlaying);
}

function stopPlayback() {
  if (state.mode === 'video' && dom.frameVideo) {
    dom.frameVideo.pause();
  }
  if (state.timer) {
    clearInterval(state.timer);
    state.timer = null;
  }
  setPlaybackStatus(false);
}

function startPlayback() {
  if (state.mode === 'video' && dom.frameVideo) {
    dom.frameVideo.playbackRate = state.fps;
    dom.frameVideo.loop = state.loop;
    dom.frameVideo.play().catch(() => {});
    setPlaybackStatus(true);
    return;
  }
  if (!currentFrames().length) return;
  if (state.timer) return;
  const interval = Math.max(1000 / state.fps, 120);
  state.timer = setInterval(() => {
    nextFrame();
  }, interval);
  setPlaybackStatus(true);
}

function togglePlayback() {
  if (state.playing) {
    stopPlayback();
  } else {
    startPlayback();
  }
}

function currentSeries() {
  if (!data || !data.series) return null;
  return data.series.find((series) => series.id === state.seriesId) || null;
}

function currentFrames() {
  const series = currentSeries();
  return series ? series.frames || [] : [];
}

function getVideoSource(series) {
  if (!series || !series.video) return null;
  const webm = series.video.webm;
  const mp4 = series.video.mp4;
  if (dom.frameVideo && webm) {
    const canPlayWebmVp9 = dom.frameVideo.canPlayType('video/webm; codecs="vp9"');
    const canPlayWebm = dom.frameVideo.canPlayType('video/webm');
    if (canPlayWebmVp9 || canPlayWebm) {
      return webm;
    }
  }
  if (mp4) return mp4;
  return webm || null;
}

function setMediaMode(mode) {
  state.mode = mode;
  if (dom.frameVideo) dom.frameVideo.hidden = mode !== 'video';
  if (dom.frameImage) dom.frameImage.hidden = mode === 'video';
}

function updateSlider() {
  const frames = currentFrames();
  dom.frameSlider.max = Math.max(frames.length - 1, 0);
  dom.frameSlider.value = Math.min(state.frameIndex, frames.length ? frames.length - 1 : 0);
}

function updateFrameDisplay() {
  const frames = currentFrames();
  if (!frames.length) {
    dom.viewerEmpty.classList.add('active');
    dom.frameImage.removeAttribute('src');
    dom.frameLabel.textContent = 'Ingen frames lastet.';
    dom.frameIndex.textContent = '0 / 0';
    dom.frameTime.textContent = '--';
    return;
  }

  dom.viewerEmpty.classList.remove('active');
  const frame = frames[state.frameIndex] || frames[0];
  if (state.mode !== 'video') {
    dom.frameImage.src = frame.src;
  }
  dom.frameLabel.textContent = frame.label || frame.time;
  dom.frameIndex.textContent = `${state.frameIndex + 1} / ${frames.length}`;
  dom.frameTime.textContent = frame.time || '--';
}

function syncFromVideo(force = false) {
  if (state.mode !== 'video' || !dom.frameVideo) return;
  const frames = currentFrames();
  if (!frames.length || !dom.frameVideo.duration) return;
  const progress = dom.frameVideo.currentTime / dom.frameVideo.duration;
  const nextIndex = Math.min(frames.length - 1, Math.round(progress * (frames.length - 1)));
  if (force || nextIndex !== state.frameIndex) {
    state.frameIndex = nextIndex;
    updateSlider();
    updateFrameDisplay();
  }
}

function setFrame(index) {
  const frames = currentFrames();
  if (!frames.length) return;
  const nextIndex = Math.max(0, Math.min(index, frames.length - 1));
  state.frameIndex = nextIndex;
  if (state.mode === 'video' && dom.frameVideo && dom.frameVideo.duration) {
    const progress = frames.length > 1 ? nextIndex / (frames.length - 1) : 0;
    dom.frameVideo.currentTime = dom.frameVideo.duration * progress;
  }
  updateSlider();
  updateFrameDisplay();
}

function nextFrame() {
  const frames = currentFrames();
  if (!frames.length) return;
  const isLast = state.frameIndex >= frames.length - 1;
  if (isLast && !state.loop) {
    stopPlayback();
    return;
  }
  const nextIndex = isLast ? 0 : state.frameIndex + 1;
  setFrame(nextIndex);
}

function prevFrame() {
  const frames = currentFrames();
  if (!frames.length) return;
  const prevIndex = state.frameIndex === 0 ? frames.length - 1 : state.frameIndex - 1;
  setFrame(prevIndex);
}

function renderSeriesButtons() {
  dom.seriesContainer.innerHTML = '';
  if (!data || !data.series || !data.series.length) return;

  data.series.forEach((series) => {
    const button = document.createElement('button');
    button.className = 'series-button';
    button.textContent = series.label;
    button.addEventListener('click', () => setSeries(series.id));
    if (series.id === state.seriesId) {
      button.classList.add('active');
    }
    dom.seriesContainer.appendChild(button);
  });
}

function setSeries(seriesId) {
  stopPlayback();
  state.seriesId = seriesId;
  state.frameIndex = 0;
  const series = currentSeries();
  const videoSrc = getVideoSource(series);
  if (videoSrc && dom.frameVideo) {
    setMediaMode('video');
    dom.frameVideo.src = videoSrc;
    dom.frameVideo.playbackRate = state.fps;
    dom.frameVideo.loop = state.loop;
    dom.frameVideo.load();
  } else {
    setMediaMode('frames');
    if (dom.frameVideo) {
      dom.frameVideo.removeAttribute('src');
      dom.frameVideo.load();
    }
  }
  renderSeriesButtons();
  updateSlider();
  updateFrameDisplay();
}

function updateStats() {
  const seriesCount = data && data.series ? data.series.length : 0;
  const frameCount = data && data.series
    ? data.series.reduce((sum, series) => sum + (series.frames ? series.frames.length : 0), 0)
    : 0;

  if (dom.statSeries) dom.statSeries.textContent = String(seriesCount);
  if (dom.statFrames) dom.statFrames.textContent = String(frameCount);
  if (dom.statFps) dom.statFps.textContent = `${state.fps.toFixed(1)}x`;
}

function applyFilters() {
  const brightness = Number(dom.brightnessInput.value || 1).toFixed(2);
  const contrast = Number(dom.contrastInput.value || 1).toFixed(2);
  dom.viewerFrame.style.setProperty('--frame-brightness', brightness);
  dom.viewerFrame.style.setProperty('--frame-contrast', contrast);
}

function bindControls() {
  dom.playToggle.addEventListener('click', togglePlayback);
  dom.prevButton.addEventListener('click', () => {
    stopPlayback();
    prevFrame();
  });
  dom.nextButton.addEventListener('click', () => {
    stopPlayback();
    nextFrame();
  });
  dom.frameSlider.addEventListener('input', (event) => {
    stopPlayback();
    setFrame(Number(event.target.value));
  });
  dom.speedInput.addEventListener('input', (event) => {
    state.fps = Number(event.target.value);
    dom.speedValue.textContent = `${state.fps.toFixed(1)}x`;
    if (state.mode === 'video' && dom.frameVideo) {
      dom.frameVideo.playbackRate = state.fps;
    } else if (state.playing) {
      stopPlayback();
      startPlayback();
    }
    updateStats();
  });
  dom.loopToggle.addEventListener('change', (event) => {
    state.loop = event.target.checked;
    if (state.mode === 'video' && dom.frameVideo) {
      dom.frameVideo.loop = state.loop;
    }
  });
  dom.brightnessInput.addEventListener('input', applyFilters);
  dom.contrastInput.addEventListener('input', applyFilters);

  if (dom.frameVideo) {
    dom.frameVideo.addEventListener('loadedmetadata', () => {
      updateSlider();
      setFrame(state.frameIndex);
    });
    dom.frameVideo.addEventListener('timeupdate', () => {
      syncFromVideo();
    });
    dom.frameVideo.addEventListener('ended', () => {
      setPlaybackStatus(false);
    });
    dom.frameVideo.addEventListener('play', () => {
      setPlaybackStatus(true);
    });
    dom.frameVideo.addEventListener('pause', () => {
      setPlaybackStatus(false);
    });
  }

  const overlayPairs = [
    { input: document.getElementById('toggle-grid'), target: dom.overlayGrid },
    { input: document.getElementById('toggle-sunpath'), target: dom.overlaySunpath },
    { input: document.getElementById('toggle-shadow'), target: dom.overlayShadow },
  ];

  overlayPairs.forEach(({ input, target }) => {
    if (!input || !target) return;
    input.addEventListener('change', (event) => {
      target.classList.toggle('hidden', !event.target.checked);
    });
  });
}

function initDefaults() {
  if (!data) return;
  state.fps = data.defaults && data.defaults.fps ? Number(data.defaults.fps) : 1;
  state.loop = data.defaults && typeof data.defaults.loop === 'boolean' ? data.defaults.loop : true;
  dom.speedInput.value = state.fps;
  dom.speedValue.textContent = `${state.fps.toFixed(1)}x`;
  dom.loopToggle.checked = state.loop;
  applyFilters();

  const initialSeries = data.defaults && data.defaults.seriesId
    ? data.defaults.seriesId
    : (data.series && data.series[0] ? data.series[0].id : null);

  if (initialSeries) {
    setSeries(initialSeries);
  } else {
    updateFrameDisplay();
  }

  updateStats();
}

async function loadData() {
  try {
    const response = await fetch(DATA_URL, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`Kunne ikke laste solstudie-data (${response.status})`);
    }
    data = await response.json();
  } catch (error) {
    console.error(error);
    data = { title: 'Solstudie', series: [], defaults: { fps: 1, loop: true } };
  }

  renderSeriesButtons();
  initDefaults();
}

bindControls();
loadData();
