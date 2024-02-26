loops = 200;
anim_in = 300;
anim_out = 100;
timer = 0;
cover_size = 200;
frequency = [];
$(document).ready(function() {
    $("#cover").css({
        height: `${cover_size}px`,
        width: `${cover_size}px`,
        left: `-${cover_size / 2}px`,
        top: `-${cover_size / 2}px`
    });
    var audio = new Audio();
    var audioContext = new (window.AudioContext || window.webkitAudioContext)();
    var analyser = audioContext.createAnalyser();
    var microphone;

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            microphone = audioContext.createMediaStreamSource(stream);
            microphone.connect(analyser);
            analyser.connect(audioContext.destination);
        })
        .catch(function(err) {
            console.error('Error accessing microphone:', err);
        });

    file.onchange = function() {
        var files = this.files;
        audio.src = URL.createObjectURL(files[0]);
        audio.load();
        audio.play();
        var context = new AudioContext();
        var src = context.createMediaElementSource(audio);

        src.connect(analyser);
        analyser.connect(context.destination);

        analyser.fftSize = 256;

        var bufferLength = analyser.frequencyBinCount;

        var dataArray = new Uint8Array(bufferLength);

        function animate() {
            requestAnimationFrame(animate);
            analyser.getByteFrequencyData(dataArray);
            //console.log(dataArray);
            for (var j = 0; j < bufferLength; j++) {
                glow_sphere_size = Math.floor(
                    Math.random() * (cover_size * 0.6) + 1
                );
                // console.log(dataArray[j]);
                for (i = 1; i < 9; i++) {
                    R = Math.floor(Math.random() * 255 + 0);
                    G = Math.floor(Math.random() * 255 + 0);
                    B = Math.floor(Math.random() * 255 + 0);
                    A = 1;
                    pow = Math.floor(dataArray[j]);
                    $(".g" + i).css({
                        background: `rgba(${R},${G},${B},0.7)`,
                        boxShadow: `0px 0px ${glow_sphere_size *
                            2}px ${glow_sphere_size /
                            2}px rgba(${R},${G},${B},${A})`,
                        transition:
                            "background 0.3s linear, box-shadow 0.3s linear"
                    });
                }
                // console.log(pow);

                if (dataArray[j] > 0 && dataArray[j] < 16) {
                    $(".g1").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `-37px`,
                            top: `-37px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g1").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 16 && dataArray[j] < 32) {
                    $(".g2").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `37px`,
                            top: `37px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g2").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 32 && dataArray[j] < 48) {
                    $(".g3").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `-37px`,
                            top: `37px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g3").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 48 && dataArray[j] < 64) {
                    $(".g4").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `37px`,
                            top: `-37px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g4").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 64 && dataArray[j] < 80) {
                    $(".g5").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `0px`,
                            top: `-50px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g5").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 80 && dataArray[j] < 96) {
                    $(".g6").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `0px`,
                            top: `50px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g6").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 96 && dataArray[j] < 112) {
                    $(".g7").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `-50px`,
                            top: `0px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g7").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                } else if (dataArray[j] > 112 && dataArray[j] < 128) {
                    $(".g8").animate(
                        {
                            width: `${pow}px`,
                            height: `${pow}px`,
                            left: `50px`,
                            top: `0px`,
                            opacity: "1"
                        },
                        anim_in
                    );
                    $(".g8").animate(
                        {
                            width: `0px`,
                            height: `0px`,
                            left: `0px`,
                            top: `0px`,
                            opacity: "0"
                        },
                        anim_out
                    );
                }
            }
        }
        audio.play();
        animate();
    };
});
