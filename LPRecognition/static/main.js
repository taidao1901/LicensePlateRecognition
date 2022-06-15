$(document).ready(function() {
  var datas=null;

  var dropContainer = document.getElementById('drop-container');
  dropContainer.ondragover = dropContainer.ondragend = function() {
    return false;
  };

  dropContainer.ondrop = function(e) {
    e.preventDefault();
    loadImage(e.dataTransfer.files[0])
  }

  $("#browse-button").change(function() {
    loadImage($("#browse-button").prop("files")[0]);
  });

  $('.modal').modal({
    dismissible: false,
    ready: function(modal, trigger) {
      $.ajax({
        type: "POST",
        url: '/LPRecognition/api_request/',
        data: {
          'image64': $('#img-card-1').attr('src')
        },
        dataType: 'text',
        success: function(data) {
          loadStats(data);
          datas = JSON.parse(data);
        },async : false
      }).always(function() {
        modal.modal('close');
      });
    }
  });
 
  $('#go-back').click(function() {
    $('#img-card-1').removeAttr("src");
    $('#stat-table').html('');
    switchCard(0);
  });
   $('#go-start').click(function() {
    $(document).ready(function(){
      $('.card crop').remove();
    });
    $('#stat-table').html('');
    switchCard(0);
  });

  $('#show').click(function() {
    switchCard(3);
    if(datas["success"] == true){
      $('#img-card-3').attr('src',datas['recog_image']);
      document.getElementById("result_text").innerHTML = datas["result"];
  }
});

  $('#upload-button').click(function() {
    $('.modal').modal('open');
  });
});

switchCard = function(cardNo) {
  var containers = [".dd-container", ".uf-container", ".dt-container", ".it-container"];
  var visibleContainer = containers[cardNo];
  for (var i = 0; i < containers.length; i++) {
    var oz = (containers[i] === visibleContainer) ? '1' : '0';
    $(containers[i]).animate({
      opacity: oz
    }, {
      duration: 200,
      queue: false,
    }).css("z-index", oz);
  }
}

loadImage = function(file) {
  var reader = new FileReader();
  reader.onload = function(event) {
    $('#img-card-1').attr('src', event.target.result);
  }
  reader.readAsDataURL(file);
  switchCard(1);  
}

loadStats = function(jsonData) {
  switchCard(2);
  var data = JSON.parse(jsonData);
  if(data["success"] == true){
    $('#img-card-2').attr('src',data['detect_image']);
  }
}


