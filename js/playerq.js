document.addEventListener('DOMContentLoaded', () => {
	var urlParams = new URLSearchParams(window['location']['search']);

    
    var src = window.atob(data.widevine);
    var url = window.atob(data.widevine);
	var type = getExt(url);
    console.log(src);
    console.log(type);
    
	switch (type) {
        case 'flv':
            playflv(url);
            break;
        case 'm3u8':
            playhls(url);
            break;
        default:
            playhls(url)
    }

function getExt(filepath){
     return filepath.split("?")[0].split("#")[0].split('.').pop();
}


function playhls(src){
    var video = document.querySelector('video');

	var defaultOptions = {};
    
	if (!Hls.isSupported()) {
		video.src = src;
		var player = new Plyr(video, defaultOptions);
	} else {
		var hls = new Hls();
		hls.loadSource(src);
    	    hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {

	      	var availableQualities = hls.levels.map((l) => l.height)
	      	availableQualities.unshift(0)

		    defaultOptions.quality = {
		    	default: 0,
		        options: availableQualities,
		        forced: true,        
		        onChange: (e) => updateQuality(e),
		    }

		    defaultOptions.i18n = {
		    	qualityLabel: {
		    		0: 'Auto',
		    	},
		    }
            
            defaultOptions.controls = ["play-large", "pause-large", "play", "mute", "volume", "live", "settings", "pip", "fullscreen"]
            defaultOptions.settings = ['quality', 'speed']
            defaultOptions.speed = {
                                        selected: 1,
                                        options: [0.5, 0.75, 1]
                                    },
            
		    hls.on(Hls.Events.LEVEL_SWITCHED, function (event, data) {
	          var span = document.querySelector(".plyr__menu__container [data-plyr='quality'][value='0'] span")
	          if (hls.autoLevelEnabled) {
	            span.innerHTML = `AUTO (${hls.levels[data.level].height}p)`
	          } else {
	            span.innerHTML = `AUTO`
	          }
	        })

		     var player = new Plyr(video, defaultOptions);
		     video.speed = 1;
         });	

	hls.attachMedia(video);
    	window.hls = hls;		 
    }

    function updateQuality(newQuality) {
      if (newQuality === 0) {
        window.hls.currentLevel = -1;
      } else {
        window.hls.levels.forEach((level, levelIndex) => {
          if (level.height === newQuality) {
            console.log("Found quality match with " + newQuality);
            window.hls.currentLevel = levelIndex;
          }
        });
      }
    }
}

function playflv(src){
    if (flvjs.isSupported()) {
      const player = document.getElementById("player");
      new Plyr(player, {
                            controls: ["play-large", "pause-large", "play", "mute", "volume", "live", "settings", "pip", "fullscreen"],
                            settings: ['speed', 'loop'],
                            speed: {
                                        selected: 1,
                                        options: [0.5, 0.75, 1]
                                    },
                        });
                        player.speed = 1;
      const flvPlayer = flvjs.createPlayer({
        type: "flv",
        url: src
      });
      flvPlayer.attachMediaElement(player);
      flvPlayer.load();
      flvPlayer.play();
    }
}

});