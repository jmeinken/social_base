crp = {}

crp.imageIndex = 0;

crp.templateEngine = function (templateId, args) {
	var args = args || {};
	var template = $('#'+templateId).html();
	if (!template) template = '';
	//console.log(templateId);
	for (arg in args) {
		var str = '[[' + arg + ']]'
		template = template.split(str).join(args[arg]);
	}
	return template;
}

crp.addCropItModal = function (inputId) {
	var args = {};
	args.id = inputId;
	//args.defaultSource = $('#'+inputId).attr('data-default-source');
	//args.label = $('#'+inputId).attr('data-label');
	//args.modalId = inputId + '-modal';
	
	//append a cropit modal
	if ( crp.aspectRatio == '1:1' ) {
		args.aspectRatioClass = 'cropit-preview-square';
	} else {
		args.aspectRatioClass = 'cropit-preview-wide';
	}
	var modalHTML = crp.templateEngine('image-modal-template', args);
	$('body').append(modalHTML);
}

crp.addCropItModalEvents = function(inputId) {
	var editorId = '#' + inputId + '-image-editor'
	
	var conf = {
    	exportZoom : crp.exportZoom,
    	maxZoom : crp.maxZoom,
    	minZoom : crp.minZoom,
    	smallImage : 'allow',
    	//imageState: { src: { imageSrc } }
    }
	
	if (!crp.multi) {
		//put start image in the modal as well
		if ( $('#'+inputId).val() ) {
			conf.imageState = { src: UPLOADS_URL_PATH + $('#'+inputId).val() }
		}
	}
	
	$(editorId).cropit(conf);
	
    $(editorId + ' .rotate-cw').click(function() {
    	$(editorId).cropit('rotateCW');
    });
    $(editorId + ' .rotate-ccw').click(function() {
		$(editorId).cropit('rotateCCW');
    });
}

crp.addMultiImageTool = function(inputId) {
	var args = {};
	args.id = inputId;
	args.label = $('#'+inputId).attr('data-label');
	args.modalId = inputId + '-modal';
	args.height = '90px';
	if ( crp.aspectRatio == '1:1' ) {
		args.width = '90px';
	} else {
		args.width = '120px';
	}
	var ImagePreviewHTML = crp.templateEngine('multi-image-preview-template', args);
	$('#'+inputId).after(ImagePreviewHTML);
}

crp.addMultiImageEvents = function(inputId) {
	var editorId = '#' + inputId + '-image-editor'
	$('#' + inputId + '-remove-image').click(function() {
		$('#' + inputId).val('');
		$('#' + inputId + '-preview').attr('src', '');
		$('#' + inputId + '-preview').hide();
		$('#' + inputId + '-remove-image').hide();
		$('#' + inputId + '-modal').modal('hide');
	});
	$('#' + inputId + '-show-picture-box').click(function() {
		$('#' + inputId + '-picture-box').slideDown();
	});
	$('#' + inputId + '-upload-image').click(function() {
		var imageUri = $(editorId).cropit('export');
		var args = {}
		args.src = imageUri
		args.imageIndex = crp.imageIndex;
		crp.imageIndex++;
		args.height = '90px';
		if ( crp.aspectRatio == '1:1' ) {
			args.width = '90px';
		} else {
			args.width = '120px';
		}
    	var imgPreview = crp.templateEngine('multi-image-image-loading-template', args);
    	$('#' + inputId + '-picture-box .multi-image-add-new').before(imgPreview);
    	$('#' + inputId + '-modal').modal('hide');
    	$.ajax({
    		url: "/images/upload",
    		data: {
    			image: imageUri,
    			base_name: 'user_image'
    		},
    		type: "POST",
    		dataType : "json",
    	})
    	.done(function( json ) {
    		console.log('success');
    		newVal = $('#' + inputId).val() + ',' + (json.name);
    		$('#' + inputId).val(newVal);
    		var args2 = {}
    		args2.src = json.path;
    		args2.height = '90px';
    		if ( crp.aspectRatio == '1:1' ) {
    			args2.width = '90px';
    		} else {
    			args2.width = '120px';
    		}
    		var imgHTML = crp.templateEngine('multi-image-image-preview-template', args2);
    		$('#' + args.imageIndex + '-image-preview').html(imgHTML);
    	})
    	.fail(function( xhr, status, errorThrown ) {
    		alert( "error" );
    		console.log( "Error: " + errorThrown );
    		console.log( "Status: " + status );
    		console.dir( xhr );
    	})
    	.always(function( xhr, status ) {
    		//run whether success or fail
    	});
	});
}

crp.addSingleImageTool = function(inputId) {
	var args = {};
	args.id = inputId;
	if ( $('#'+inputId).val() ) {
		args.defaultSource = UPLOADS_URL_PATH + $('#'+inputId).val()
	} else {
		args.defaultSource = $('#'+inputId).attr('data-default-source');
	}
	args.label = $('#'+inputId).attr('data-label');
	args.modalId = inputId + '-modal';
	var ImagePreviewHTML = crp.templateEngine('image-preview-template', args);
	$('#'+inputId).after(ImagePreviewHTML);
	if ( args.defaultSource ) {
    	$('#' + inputId + '-preview').show();
    	$('#' + inputId + '-remove-image').show();
    } 
	
}

crp.addSingleImageEvents = function(inputId) {
	var args = {};
	args.id = inputId;
	var editorId = '#' + inputId + '-image-editor'
	$('#' + inputId + '-remove-image').click(function() {
		$('#' + inputId).val('');
		$('#' + inputId + '-preview').attr('src', '');
		$('#' + inputId + '-preview').hide();
		$('#' + inputId + '-remove-image').hide();
		$('#' + inputId + '-modal').modal('hide');
	});
	$('#' + inputId + '-upload-image').click(function() {
    	var imageUri = $(editorId).cropit('export');
    	$('#' + inputId + '-preview').attr('src', imageUri).css({ opacity: 0.3 }).show();
    	var loadingIconHTML = crp.templateEngine('loading-icon-template', args);
    	$('#' + inputId + '-preview-box').append(loadingIconHTML);
    	$('#' + inputId + '-modal').modal('hide');
    	$.ajax({
    		url: "/images/upload",
    		data: {
    			image: imageUri,
    			base_name: 'user_image'
    		},
    		type: "POST",
    		dataType : "json",
    	})
    	.done(function( json ) {
    		$('#' + inputId).val(json.name);
    		$('#' + inputId + '-loading-icon').remove();
    		$('#' + inputId + '-preview').attr('src', json.path).css({ opacity: 1.0 });
    		$('#' + inputId + '-remove-image').show();
    	})
    	.fail(function( xhr, status, errorThrown ) {
    		alert( "error" );
    		console.log( "Error: " + errorThrown );
    		console.log( "Status: " + status );
    		console.dir( xhr );
    	})
    	.always(function( xhr, status ) {
    		//run whether success or fail
    	});
	});
}

crp.appendCropItTool = function (inputId) {
	crp.exportZoom = $('#'+inputId).attr('data-export-zoom') || 1;
	crp.minZoom = $('#'+inputId).attr('data-min-zoom') || 'fit';
	crp.maxZoom = $('#'+inputId).attr('data-max-zoom') || 5;
	crp.aspectRatio = $('#'+inputId).attr('data-aspect-ratio') || '4:3';
	
	if ( $('#'+inputId).attr('data-multiple-allowed') ) {
		crp.multi = true;
	} else {
		crp.multi = false;
	}
	
	
	crp.addCropItModal(inputId);
	crp.addCropItModalEvents(inputId);
	
	if ( crp.multi ) {
		crp.addMultiImageTool(inputId);
		crp.addMultiImageEvents(inputId);
	} else {
		crp.addSingleImageTool(inputId);
		crp.addSingleImageEvents(inputId);
	}
}



$(document).ready(function() {
	
	$('.image_input').each(function(index) {
		//create crop-it tool for all image inputs
		var inputId = $(this).attr('id');
		crp.appendCropItTool(inputId);
	});

});