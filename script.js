
async function loadVideos() {
    try {
        const response = await fetch('./videos.csv');
        const data = await response.text();

        videos = Papa.parse(data, {
            header: true,
            skipEmptyLines: true
        }).data;

        return videos;
    } catch (error) {
        console.error('Error fetching the CSV file:', error);
    }
}

function populateLanguagesGrid() {
    const languagesGrid = document.getElementById('languages-grid');
    const uniqueLanguages = [...new Set(videos.map(video => video.language))];
    uniqueLanguages.sort((a, b) => a.localeCompare(b));

    for (const language of uniqueLanguages) {
        const link = document.createElement('a');
        link.href = `browse.html?language=${encodeURIComponent(language)}`;
        link.textContent = language;
        languagesGrid.appendChild(link);
    }
}


function initializeBrowsePage(){
    const videosGrid = document.getElementById('videos-grid');

    const urlParams = new URLSearchParams(window.location.search);
    window.selectedLanguage = urlParams.get('language');
    window.videos = videos.filter(video => video.language === selectedLanguage)
    console.log(videos);

    const titleElement = document.getElementById('page-title');
    titleElement.textContent = `${selectedLanguage} Videos`;

    populateChannelFilterOptions();
    populateVideosGrid();
}

function populateChannelFilterOptions(){
    const channelFilter = document.getElementById('channel-filter');
    const channels = [...new Set(videos.map(video => video.channel_title))].sort();

    for(var channel of channels){
        const channelOption = document.createElement('option');
        channelOption.value = channel;
        channelOption.innerHTML = channel;
        channelFilter.appendChild(channelOption);
    }
    $('#channel-filter').selectpicker('refresh');
}

function populateVideosGrid() {
    //filter videos
    const filteredChannels = $('#channel-filter').selectpicker('val');
    var filteredVideos = null;
    filteredVideos = filteredChannels ? videos.filter(video => filteredChannels?.includes(video.channel_title)) : videos;

    //Sort Videos
    const sortByElement = document.getElementById('sort-by');
    const sortBy = sortByElement.value;

    orderedVideos = filteredVideos.sort((a, b) => {
        const dateA = new Date(a.upload_date);
        const dateB = new Date(b.upload_date);
        
        switch(sortBy){
            case 'newestFirst':
                return dateB - dateA;
            case 'oldestFirst':
                return dateA - dateB;
            case 'random':
                return Math.random() - 0.5;
        }

      });


    //Populate videos
    const videosGrid = document.getElementById('videos-grid');
    videosGrid.innerHTML = '';
    if (videos.length > 0) {
        for (video of filteredVideos) {
            const videoItem = document.createElement('div');
            videoItem.classList.add('video-item');

            const thumbnail = document.createElement('img');
            thumbnail.src = `https://img.youtube.com/vi/${video.video_id}/mqdefault.jpg`;
            thumbnail.alt = `${video.title} Thumbnail`;
            thumbnail.classList.add('video-thumbnail');

            const videoInfo = document.createElement('div');
            videoInfo.classList.add('video-info');

            const titleElement = document.createElement('div');
            titleElement.classList.add('video-title');
            titleElement.textContent = video.title;

            const channelElement = document.createElement('div');
            channelElement.classList.add('video-channel');
            channelElement.textContent = `${video.channel_title}`;



            const linkWrapper = document.createElement('a');
            linkWrapper.href = `watch.html?video_id=${video.video_id}&title=${encodeURIComponent(video.title)}&language=${encodeURIComponent(selectedLanguage)}`;


            videoInfo.appendChild(titleElement);
            videoInfo.appendChild(channelElement);

            videoItem.appendChild(thumbnail);
            videoItem.appendChild(videoInfo);

            linkWrapper.appendChild(videoItem)

            videosGrid.appendChild(linkWrapper);
        }
    } else {
        window.location.replace('index.html');
    }
}



