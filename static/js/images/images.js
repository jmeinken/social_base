crp = {}

crp.imageIndex = 0;
crp.inputIds = [];			// track which elements have already been added

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

crp.parseImageList = function (inputId) {
	var listStr = $('#' + inputId).val();
	result = listStr.split(/[,\s]+/).filter(function(v){return v!==''});
	return result;
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
	
	$(editorId).unbind().cropit(conf);
	
    $(editorId + ' .rotate-cw').unbind().click(function() {
    	$(editorId).cropit('rotateCW');
    });
    $(editorId + ' .rotate-ccw').unbind().click(function() {
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
	var existingImages = crp.parseImageList(inputId);
	if (existingImages.length > 0) {
		$('#' + inputId + '-picture-box').slideDown();
	}
	for (var i=0; i<existingImages.length; i++) {
		console.log(existingImages[i]);
		var args2 = {}
		args2.src = UPLOADS_URL_PATH + existingImages[i];
		args2.imgName = existingImages[i];
		args2.imageIndex = crp.imageIndex;
		args2.height = '90px';
		args2.inputId = inputId;
		if ( crp.aspectRatio == '1:1' ) {
			args2.width = '90px';
		} else {
			args2.width = '120px';
		}
		var imgHTML = crp.templateEngine('multi-image-image-preview-template', args2);
		$('#' + inputId + '-picture-box .multi-image-add-new').before(imgHTML);
		crp.imageIndex++;
	}
	$('.remove-image').unbind().click(function() {
		var previewId = $(this).attr('data-delete-id');
		var imgName = $('#'+previewId).attr('data-image-name');
		var matchingInputId = $('#'+previewId).attr('data-input-id');
		var imgListStr = $('#'+matchingInputId).val();
		console.log('removing image');
		console.log(previewId);
		console.log(imgName);
		console.log(inputId);
		imgListStr = imgListStr.replace(imgName,'');
		$('#'+matchingInputId).val(imgListStr);
		$('#'+previewId).remove();
	});
	
	
}

crp.addMultiImageEvents = function(inputId) {
	var editorId = '#' + inputId + '-image-editor'
	$('#' + inputId + '-remove-image').unbind().click(function() {
		$('#' + inputId).val('');
		$('#' + inputId + '-preview').attr('src', '');
		$('#' + inputId + '-preview').hide();
		$('#' + inputId + '-remove-image').hide();
		$('#' + inputId + '-modal').modal('hide');
	});
	$('#' + inputId + '-show-picture-box').unbind().click(function() {
		$('#' + inputId + '-picture-box').slideDown();
	});
	$('#' + inputId + '-upload-image').unbind().click(function() {
		var imageUri = $(editorId).cropit('export');
		var args = {}
		args.src = imageUri
		args.imageIndex = crp.imageIndex;
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
    			base_name: crp.baseName
    		},
    		type: "POST",
    		dataType : "json",
    	})
    	.done(function( json ) {
    		newVal = $('#' + inputId).val() + ',' + (json.name);
    		$('#' + inputId).val(newVal);
    		var args2 = {}
    		args2.src = json.path;
    		args2.imgName = json.name;
    		args2.imageIndex = crp.imageIndex;
    		args2.height = '90px';
    		args2.inputId = inputId;
    		if ( crp.aspectRatio == '1:1' ) {
    			args2.width = '90px';
    		} else {
    			args2.width = '120px';
    		}
    		var imgHTML = crp.templateEngine('multi-image-image-preview-template', args2);
    		$('#' + crp.imageIndex + '-image-preview').replaceWith(imgHTML);
    		$('.remove-image').unbind().click(function() {
    			var previewId = $(this).attr('data-delete-id');
    			var imgName = $('#'+previewId).attr('data-image-name');
    			var imgListStr = $('#'+inputId).val();
    			imgListStr = imgListStr.replace(imgName,'');
    			$('#'+inputId).val(imgListStr);
    			$('#'+previewId).remove();
    		});
    		crp.imageIndex++;
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
	if ( $('#'+inputId).attr('data-label') ) {
		args.label = '<label>' + $('#'+inputId).attr('data-label') + '</label>';
	} else {
		args.label = '';
	}
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
	$('#' + inputId + '-remove-image').unbind().click(function() {
		$('#' + inputId).val('');
		$('#' + inputId + '-preview').attr('src', '');
		$('#' + inputId + '-preview').hide();
		$('#' + inputId + '-remove-image').hide();
		$('#' + inputId + '-modal').modal('hide');
	});
	$('#' + inputId + '-upload-image').unbind().click(function() {
    	var imageUri = $(editorId).cropit('export');
    	$('#' + inputId + '-preview').attr('src', imageUri).css({ opacity: 0.3 }).show();
    	var loadingIconHTML = crp.templateEngine('loading-icon-template', args);
    	$('#' + inputId + '-preview-box').append(loadingIconHTML);
    	$('#' + inputId + '-modal').modal('hide');
    	$.ajax({
    		url: "/images/upload",
    		data: {
    			image: imageUri,
    			base_name: crp.baseName
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
	crp.multi = ( $('#'+inputId).attr('data-multiple-allowed') === "yes" );
	crp.baseName = $('#'+inputId).attr('data-base-name') || 'image';

	
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

crp.load = function() {
	$('.image_input').each(function(index) {
		//create crop-it tool for all image inputs
		var inputId = $(this).attr('id');
		if ( $.inArray(inputId, crp.inputIds) === -1 ) {
			crp.appendCropItTool(inputId);
			crp.inputIds.push(inputId);
		}
	});
}

$(document).ready(function() {
	crp.load();
	
	
});