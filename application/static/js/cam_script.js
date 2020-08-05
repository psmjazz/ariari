var kp = {
  "nose" : 0, "leftEye" : 1, "righteye" : 2,
  "leftEar" : 3, "rightEar" : 4, "leftShoulder" : 5,
  "rightShoulder" : 6, "leftElbow" : 7, "rightElbow" : 8,
  "leftWrist" : 9, "rightWrist" : 10, "leftHip" : 11,
  "rightHip" : 12, "leftKnee" : 13, "rightKnee" : 14,
  "leftAnkle" : 15, "rightAnkle" : 16
};

var skeleton = [
  ['leftShoulder', 'rightShoulder'],
  ['leftShoulder', 'leftElbow'],
  ['rightShoulder', 'rightElbow'],
  ['leftElbow','leftWrist'],
  ['rightElbow', 'rightWrist'],
  ['leftShoulder', 'leftHip'],
  ['rightShoulder', 'rightHip'],
  ['leftHip', 'rightHip'],
  ['leftHip', 'leftKnee'],
  ['rightHip', 'rightKnee'],
  ['leftKnee', 'leftAnkle'],
  ['rightKnee', 'rightAnkle']
];

(async function() {

  // socketio 준비
  var socket = io();
  socket.on('connect', function(){
    console.log('socket start')
    socket.send({data:'connect!'});
    console.log('socket connected')
  })

  var canvas = document.getElementById('canvas'),
  context = canvas.getContext('2d'),
  video = document.createElement('video'),
  vendorUrl = window.URL || window.webkitURL;
  const net = await posenet.load();

  var width = canvas.width, height = canvas.height

  var tmp = document.createElement('canvas');
  tmp.width = width, tmp.height = height;
  var tmpctx = tmp.getContext('2d');

  var stopButton = document.getElementById('stop');
  var control = true;

  var cntText = document.getElementById('count');
  var cnt = 0;
  
  context.fillStyle = "red"
  context.lineWidth = 7;
  context.strokeStyle = '#ff0000';

  navigator.getMedia =  (navigator.getUserMedia ||
                      navigator.webkitGetUserMedia ||
                      navigator.mozGetuserMedia ||
                      navigator.msGetUserMedia);
  
  navigator.getMedia({
    video: true,
    audio: false
  }, function(stream) {
    video.srcObject = stream;
    video.play();
  }, function(error) {
    // an error occurred
  } );

  // navigator.getMedia({
  //   video: true,
  //   audio: false
  // }).then(function(stram){
  //   video.srcObject = stream;
  //   video.play();
  // }).catch(function(error){
  //   // an error occurred
  //   console.log(error)
  // });

  // 비디오 이벤트 리스너
  video.addEventListener('play', function() {
    draw( this, context, tmpctx, width, height );
  }, false );
  // 스탑버튼 이벤트 리스너
  stopButton.addEventListener('click', function(){
    control = false;
    socket.disconnect();
  }, )
  // 서버 -> 웹의 정확도 등 수신
  socket.on('pose-result', function(){
    console.log('rep!!');
    cntText.textContent = cnt;
    cnt+=1;
  })

  async function draw_sk(video, context, pose, score = 0.3){
    
    // video 이미지 그리기
    context.drawImage( video, 0, 0, width, height );
    if(pose['score'] < score){
      return;
    }
    // 키포인트 그리기
    // pose['keypoints'].forEach( (keypoint, idx) =>{
    //   pos = keypoint['position'];
    //   context.fillRect(pos['x']-5, pos['y']-5, 10, 10);
    // });
    // 스켈레톤 그리기
    skeleton.forEach( (sk) =>{
      start = pose['keypoints'][kp[sk[0]]];
      end = pose['keypoints'][kp[sk[1]]];
      if(start['score'] >= score && end['score'] >= score){
        context.beginPath();
        context.moveTo(start['position']['x'], start['position']['y']);
        context.lineTo(end['position']['x'], end['position']['y']);
        context.stroke();
      }

    });
    
  }

  async function draw( video, context, tmpctx, width, height ) {
    var image;
    
    // 비디오 이미지를 임시 canvas에 그림
    tmpctx.drawImage( video, 0, 0, width, height );
    image = await tmpctx.getImageData( 0, 0, width, height );
    
    // estimateSinglePose가 된 프레임만 그리기 위해서
    // 원래는 video도 estimateSinglePose에 넣을 수 있는데
    // 왠진 몰라도 예측이 안됨 예: x = 0, y = 0로만 나옴
    const pose = await net.estimateSinglePose(image, scaleFactor = 1, flipHorizontal = true, outputStride = 8);

    // console.dir(pose)

    // socketio를 통해 스켈레톤 데이터 전달
    socket.emit('skeleton-data', pose);
    // draw_sk가 하는 일 : canvas에 video 이미지 그리기, 스켈레톤 그리기
    draw_sk(video, context, pose, 0.5);
    // console.log('send')
    if(control)
      setTimeout( draw, 10, video, context, tmpctx, width, height );
  }

} )();
