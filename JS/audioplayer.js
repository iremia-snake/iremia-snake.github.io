class AudioPlayer{
    constructor(container) {
        this.container = container;
        this.audio = container.getElementsByTagName('audio')[0];
        this.playBtn = container.querySelector('.audio-player-button');
        this.slider = container.querySelector('.audio-player-slider');
        this.sliderPoint = container.querySelector('.audio-player-slider-point');
        this.init();
    }
    init(){
        this.playBtn.addEventListener('click', () => this.togglePlay());
        this.slider.addEventListener('click', (e) => this.setProgress(e));
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('loadedmetadata', () => this.updateProgress());
        this.audio.addEventListener('ended', () => this.onEnded());
    }

    togglePlay() {
        if (this.audio.paused) {
            this.audio.play();
            this.playBtn.classList.remove('play');
            this.playBtn.classList.add('pause');
        } else {
            this.audio.pause();
            this.playBtn.classList.remove('pause');
            this.playBtn.classList.add('play');
        }
    }

    setProgress(e) {
        const rect = this.slider.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        const newTime = percent * this.audio.duration;
        this.audio.currentTime = newTime;
        this.updateProgress();
    }
    updateProgress() {
        if (!this.audio.duration) return;
        const percent = (this.audio.currentTime / this.audio.duration) * 100;
        this.sliderPoint.style.left = percent + '%';
        this.sliderPoint.style.transform = 'translateX(-'+percent+'%)'
        this.slider.style.setProperty('--progress', percent + '%');
        this.slider.style.background = `linear-gradient(to right, var(--very-dark-color) ${percent}%, var(--primary-color) ${percent}%)`;
    }
    onEnded() {
        this.playBtn.classList.remove('pause');
        this.playBtn.classList.add('play');
        this.audio.currentTime = 0;
        this.updateProgress();
    }
}

window.addEventListener('load', ()=>{
    Array.from(document.body.querySelectorAll('.audio-player')).forEach(element => {
        new AudioPlayer(element);
    });

})
