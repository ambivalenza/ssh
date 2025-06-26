document.addEventListener('DOMContentLoaded', function() {
  const wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#0d6efd',
    progressColor: '#0b5ed7',
    cursorColor: '#495057',
    height: 80
  });
  
    wavesurfer.load('{{ track.audio_file.url }}');
  // Кнопки управления
  document.getElementById('playBtn').addEventListener('click', () => wavesurfer.play());
  document.getElementById('pauseBtn').addEventListener('click', () => wavesurfer.pause());
});