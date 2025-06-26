<div id="waveform">
  <!-- the waveform will be rendered here -->
</div>

<script type="module">
import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js'

const wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: '#4F4A85',
  progressColor: '#383351',
  url: '/audio.mp3',
})

wavesurfer.on('interaction', () => {
  wavesurfer.play()
})
</script>