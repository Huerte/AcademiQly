const APP_ID = "de6a7153fb7d4dddb4e017a710e10c40";
const TOKEN = "007eJxTYKhO/fo3y5anLsMsakvWn6yl+3KK1PR+tJeZcPkHZx7Rz1NgSEk1SzQ3NDVOSzJPMUlJSUkySTUwNAcKGaQaGiSbGOw4pJzZEMjIUDE7i5WRAQJBfC4Gx+TElNTczMKcSgYGAOz3ITQ=";
const CHANNEL = "Academiqly";

const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });

let localTracks = {};
let remoteUsers = {};

let joinAndDisplayLocalStream = async () => {

    client.on("user-published", handleuserJoined);

    let uid = await client.join(APP_ID, CHANNEL, TOKEN, null);

    localTracks.audioTrack = await AgoraRTC.createMicrophoneAudioTrack();
    localTracks.videoTrack = await AgoraRTC.createCameraVideoTrack();

    let player = `<div class="video-container" id="user-container-${uid}">
                    <div class="video-player" id="user-${uid}"></div>
                 </div>`;
    document.getElementById("video-streams")
            .insertAdjacentHTML("beforeend", player);


    localTracks.videoTrack.play(`user-${uid}`);

    await client.publish([localTracks.audioTrack, localTracks.videoTrack]);

};

let joinStream = async () => {
    await joinAndDisplayLocalStream();  

    document.getElementById("join-btn").style.display = 'none';
    document.getElementById("stream-controls").style.display = 'block';
};

let handleuserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user;
    await client.subscribe(user, mediaType);

    if (mediaType === "video") {
        let player = document.getElementById(`user-container-${user.uid}`);
        if (player === null) {
            player.remove();
        }

        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="video-player" id="user-${user.uid}"></div>
                  </div>`;
        document.getElementById("video-streams").insertAdjacentElement("beforeend", player);

        user.videoTrack.play(`user-${user.uid}`);
    }

    if (mediaType === "audio") {
        user.audioTrack.play();
    }
};

let handleuserLeft = async (user) => {
    delete remoteUsers[user.uid];
    document.getElementById(`user-container-${user.uid}`).remove();
};

let leaveAndRemoveLocalStream = async () => {
    for (let trackName in localTracks) {
        let track = localTracks[trackName];
        if (track) {
            track.stop();
            track.close();
            localTracks[trackName] = null;
        }
    }

    await client.leave();
    
    document.getElementById("join-btn").style.display = "block";
    document.getElementById("stream-controls").style.display = "none";
    document.getElementById("video-streams").innerHTML = "";

};

let toggleMic = async (e) => {
    if (localTracks.audioTrack.enabled) {
        await localTracks.audioTrack.setEnabled(false);
        e.target.innerText = "Mic off";
        e.target.style.backgroundColor = "red";
    } else {
        await localTracks.audioTrack.setEnabled(true);
        e.target.innerText = "Mic On";
        e.target.style.backgroundColor = "grey";
    }
};

let toggleCamera = async (e) => {
    if (localTracks.videoTrack.enabled) {
        await localTracks.videoTrack.setEnabled(false);
        e.target.innerText = "Camera off";
        e.target.style.backgroundColor = "red";
    } else {
        await localTracks.videoTrack.setEnabled(true);
        e.target.innerText = "Camera On";
        e.target.style.backgroundColor = "grey";
    }
};

document.getElementById("join-btn").addEventListener("click", joinStream);
document.getElementById("leave-btn").addEventListener("click", leaveAndRemoveLocalStream);
document.getElementById("mic-btn").addEventListener("click", toggleMic);
document.getElementById("camera-btn").addEventListener("click", toggleCamera);