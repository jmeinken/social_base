
// requires jQuery, FontAwesome, CropIt




$ = jQuery;
mf = {}




/// PARAMETERS ////////////////////////////////////////////////////////////////////////////////

mf.uid = 0;				//set by data-user attr on #microfeed-container
mf.thread = 1;			//set by data-thread attr on #microfeed-container
mf.lastPostId = 0;
mf.postCount = 10;
mf.showMoreOption = true;
mf.addPostOption = true;
mf.subfolder = "";
mf.images = [];

mf.postImages = {}
mf.currentPostImageIndex = 0;
mf.currentPostImages = 0;

/// UTILITIES /////////////////////////////////////////////////////////////////////////////////

mf.templateEngine = function (templateId, args) {
	args = args || {};
	var template = $('#'+templateId).html();
	if (!template) template = '';
	//console.log(templateId);
	for (arg in args) {
		var str = '[[' + arg + ']]'
		template = template.split(str).join(args[arg]);
	}
	return template;
}


var mf_scripts = document.getElementsByTagName("script");
var mf_script = mf_scripts[mf_scripts.length-1];

mf.currentDirPath = function() {
	var str = mf_script.src;
	console.log(str.substring(0, str.lastIndexOf("/")));
	return str.substring(0, str.lastIndexOf("/"));
}

/// FUNCTIONS //////////////////////////////////////////////////////////////////////////////////

mf.displayPost = function(objPost, order) {
	//console.log(json.test);
	var args = objPost;  //postId, uid, username, userImage, body
	args.currentUid = mf.uid
	if (args.post_type == 'event') {
		var result = mf.templateEngine('event-post-template', args);
	} else {
		var result = mf.templateEngine('post-template', args);
	}
	if (order == 'top') {
		$('#output').prepend(result);
	} else {
		$('#output').append(result);
	}
	if ( mf.allowComments ) {
		var result = mf.templateEngine('comment-container-template', args);
		$('#comment-container-' + args.postId).append(result);
	}
	//append event times
	if (args.post_type == 'event') {
		for (var i=0; i<args.times.length; i++) {
			args1 = {}
			args1.startDate = args.times[i].startDate
			args1.timeRange = args.times[i].startTime
			if (args.times[i].endTime) {
				args1.timeRange = args.times[i].startTime + ' to ' + args.times[i].endTime
			}
			$('#event-times-' + args.postId).append( mf.templateEngine('event-times-template', args1) );
		}
	}
	if (mf.uid != 0) {
		var result = mf.templateEngine('comment-form-template', args);
	} else {
		var result = mf.templateEngine('comment-form-login-template', args);
	}
	$('#comment-form-block-'+args.postId).append(result);
	//append post options
	if (args.post_type == 'standard') {
		var postUserOptionsStr = mf.templateEngine('post-user-options-template', args);
		if (args.editable) {
			$('#post-user-options-'+args.postId).html(postUserOptionsStr);
		}
	}
	//append images
	var imageCount = objPost.images.length
	mf.postImages[objPost.postId] = objPost.images
	if (imageCount == 1) {
		args2 = {
			postId : objPost.postId,
			image1 : objPost.images[0]
		}
		var result2 = mf.templateEngine('post-image-thumbnails-template-1', args2);
		$('#post-image-thumbnails-block-'+args.postId).append(result2);
	}
	if (imageCount == 2) {
		args2 = {
			postId : objPost.postId,
			image1 : objPost.images[0],
			image2 : objPost.images[1]
		}
		var result2 = mf.templateEngine('post-image-thumbnails-template-2', args2);
		$('#post-image-thumbnails-block-'+args.postId).append(result2);
	}
	if (imageCount == 3) {
		args2 = {
			postId : objPost.postId,
			image1 : objPost.images[0],
			image2 : objPost.images[1],
			image3 : objPost.images[2],
		}
		var result2 = mf.templateEngine('post-image-thumbnails-template-3', args2);
		$('#post-image-thumbnails-block-'+args.postId).append(result2);
	}
	if (imageCount >= 4) {
		args2 = {
			postId : objPost.postId,
			image1 : objPost.images[0],
			image2 : objPost.images[1],
			image3 : objPost.images[2],
			extra : imageCount - 2
		}
		var result2 = mf.templateEngine('post-image-thumbnails-template-4', args2);
		$('#post-image-thumbnails-block-'+args.postId).append(result2);
	}
	// append comments
	var commentCount = objPost.comments.length
	if (commentCount > 4) {
		var hiddenCommentBlock = mf.templateEngine('hidden-comments-template', args);
		//alert(result2);
		$('#comments-'+objPost.postId).append(hiddenCommentBlock);
		for (var j=0; j<commentCount; j++) {
			var args2 = objPost.comments[j];
			var result2 = mf.templateEngine('comment-template', args2);
			if (j < commentCount-3) {
				$('#hidden-comments-block-'+objPost.postId).append(result2);
			} else {
				$('#comments-'+objPost.postId).append(result2);
			}
			//append comment options
			var commentUserOptionsStr = mf.templateEngine('comment-user-options-template', args2);
			if (objPost.comments[j].editable) {
				$('#comment-user-options-'+objPost.comments[j].commentId).html(commentUserOptionsStr);
			}
		}
	} else {
		for (var j=0; j<commentCount; j++) {
			var args2 = objPost.comments[j];
			var result2 = mf.templateEngine('comment-template', args2);
			$('#comments-'+objPost.postId).append(result2);
			//append comment options
			var commentUserOptionsStr = mf.templateEngine('comment-user-options-template', args2);
			if (objPost.comments[j].editable) {
				$('#comment-user-options-'+objPost.comments[j].commentId).html(commentUserOptionsStr);
			}
		}
	}
	
}


/// EVENTS /////////////////////////////////////////////////////////////////////////////////////

mf.appendEvents = function() {
	mf.appendPostEvents();
	mf.appendCommentEvents();
	mf.appendImageEvents();
}

mf.appendImageEvents = function() {
	$('#add-image-btn').unbind();
	$('#add-image-btn').click(function() {
		imageUri = $('.image-editor').cropit('export');
		mf.images.push(imageUri);
		args = {
			index : mf.images.length - 1,
			alt : 'preview',
			imageUri : imageUri
		}
		$('#image-placeholder').remove();
		var imgString = mf.templateEngine('image-preview-template', args);
		$('#new-post-image-block').append(
			imgString
		);
		var imgString = mf.templateEngine('image-placeholder-template', {});
		$('#new-post-image-block').append(
			imgString
		);
		//$('#my-img-' + mf.images.length).attr('src', mf.images[0]);
		$('#add-image-modal').modal('hide');
		mf.appendEvents();
	});
	
	//$('.remove-image').unbind();
	//$('.remove-image').click(function() {
	//	var index = $(this).attr('data-image-index');
	//	mf.images.splice(index, 1);
	//	$('#image-preview-'+index).remove();
	//});
	
	$('.show-post-image-modal').unbind();
	$('.show-post-image-modal').click(function() {
		var postId = $(this).attr('data-post-id');
		mf.currentPostImages = mf.postImages[postId];
		mf.currentPostImageIndex = 0;
		var count = mf.currentPostImages.length;
		$('#post-images-modal .modal-title').html('1 / '+count);
		$('#post-images-modal-image').attr('src',mf.postImages[postId][0]);
		$('#post-images-modal').modal('show');
		$('#post-images-scroll-backward').hide();
		if (count > 1) {
			$('#post-images-scroll-forward').show();
		} else {
			$('#post-images-scroll-forward').hide();
		}
	});
	
	$('#post-images-scroll-backward').unbind();
	$('#post-images-scroll-backward').click(function() {
		mf.currentPostImageIndex--;
		var count = mf.currentPostImages.length;
		$('#post-images-modal .modal-title').html(mf.currentPostImageIndex+1 + ' / ' + count);
		$('#post-images-modal-image').attr('src',mf.currentPostImages[mf.currentPostImageIndex]);
		$('#post-images-scroll-forward').show();
		if (mf.currentPostImageIndex > 0) {
			$('#post-images-scroll-backward').show();
		} else {
			$('#post-images-scroll-backward').hide();
		}
	});
	
	$('#post-images-scroll-forward').unbind();
	$('#post-images-scroll-forward').click(function() {
		mf.currentPostImageIndex++;
		var count = mf.currentPostImages.length;
		$('#post-images-modal .modal-title').html(mf.currentPostImageIndex+1 + ' / ' + count);
		$('#post-images-modal-image').attr('src',mf.currentPostImages[mf.currentPostImageIndex]);
		$('#post-images-scroll-backward').show();
		if (count > mf.currentPostImageIndex+1) {
			$('#post-images-scroll-forward').show();
		} else {
			$('#post-images-scroll-forward').hide();
		}
	});
	
}

mf.appendCommentEvents = function() {
	$('.new-comment-form').unbind();
	$('.new-comment-form').submit(function(e) {
		var postId = $(this).attr('data-post-id');
		//alert(postId);
		var data = $("#new-comment-form-"+postId).serialize();		// post_id, uid, body
		var url = mf.subfolder + "/microfeed/posts/comments/new";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var args = json;
			var result = mf.templateEngine('comment-template', args);
			$('#comments-'+json.postId).append(result);
			$("#new-comment-form-"+json.postId+' textarea[name=body]').val('');
			//append comment options
			var commentUserOptionsStr = mf.templateEngine('comment-user-options-template', args);
			if (args.editable) {
				$('#comment-user-options-'+args.commentId).html(commentUserOptionsStr);
			}
			mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$('.edit-comment-btn').unbind();
	$('.edit-comment-btn').click(function(e) {
		var commentId = $(this).attr('data-comment-id');
		$('#comment-'+commentId).hide();
		$('#edit-comment-'+commentId).show();
		e.preventDefault();
	});
	
	$('.delete-comment-btn').unbind();
	$('.delete-comment-btn').click(function(e) {
		var commentId = $(this).attr('data-comment-id');
		$('#delete-comment-id').val(commentId);
		$('#delete-comment-modal').modal('show');
		e.preventDefault();
	});
	
	$('.cancel-edit-comment').unbind();
	$('.cancel-edit-comment').click(function() {
		var commentId = $(this).attr('data-comment-id');
		$('#edit-comment-'+commentId).hide();
		$('#comment-'+commentId).show();
	});
	
	$(".edit-comment-form").unbind();
	$(".edit-comment-form").submit(function(e) {
		var commentId = $(this).attr('data-comment-id');
		var data = $("#edit-comment-form-"+commentId).serialize();		// post_id, body
		var url = mf.subfolder + "/microfeed/posts/comments/edit";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var commentId = json.commentId;
			$('#comment-body-'+commentId).html(json.formatted_body);
			$('#edit-comment-'+commentId).hide();
			$('#comment-'+commentId).show();
			mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$("#delete-comment-form").unbind();
	$("#delete-comment-form").submit(function(e) {
		var data = $('#delete-comment-form').serialize();		// post_id, body
		var url = mf.subfolder + "/microfeed/posts/comments/delete";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var commentId = json.commentId;
			$('#comment-block-'+commentId).html('<div class="alert alert-dismissible alert-warning"><button type="button" class="close" data-dismiss="alert">&times;</button>Comment successfully deleted.</div>');
			$('#delete-comment-modal').modal('hide');
			//mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$('.show-hidden-comments').unbind();
	$('.show-hidden-comments').click(function(e) {
		postId = $(this).attr('data-post-id');
		$('#hidden-comments-block-'+postId).show();
		$(this).parent().remove();
		e.preventDefault();
	});
}

mf.appendPostEvents = function() {
	
	$('#new-post-form').unbind();
	$("#new-post-form").submit(function(e) {
		$('#new-post-btn')
			.attr('disabled','disabled')
			.addClass('disabled')
			.html('<i class="fa fa-spinner fa-pulse fa-fw"></i> Uploading');
		var data = $("#new-post-form").serialize();		// uid, body, images[]
		data += '&thread=' + mf.thread;
		var url = mf.subfolder + "/microfeed/posts/new";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			mf.displayPost(json, 'top');
			$("#new-post-form textarea[name=body]").val('');
			$('#new-post-image-block').html('');
			$('#new-post-btn')
				.removeAttr('disabled')
				.removeClass('disabled')
				.html('Share');
			mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$('.edit-post-btn').unbind();
	$('.edit-post-btn').click(function(e) {
		var postId = $(this).attr('data-post-id');
		$('#post-'+postId).hide();
		$('#edit-post-'+postId).show();
		e.preventDefault();
	});
	
	$('.delete-post-btn').unbind();
	$('.delete-post-btn').click(function(e) {
		var postId = $(this).attr('data-post-id');
		$('#delete-post-id').val(postId);
		$('#delete-post-modal').modal('show');
		e.preventDefault();
	});
	
	$('.cancel-edit-post').unbind();
	$('.cancel-edit-post').click(function() {
		var postId = $(this).attr('data-post-id');
		$('#edit-post-'+postId).hide();
		$('#post-'+postId).show();
	});
	
	$(".edit-post-form").unbind();
	$(".edit-post-form").submit(function(e) {
		var postId = $(this).attr('data-post-id');
		var data = $("#edit-post-form-"+postId).serialize();		// post_id, body
		var url = mf.subfolder + "/microfeed/posts/edit";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var postId = json.postId;
			$('#post-body-'+postId).html(json.formatted_body);
			$('#edit-post-'+postId).hide();
			$('#post-'+postId).show();
			mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$("#delete-post-form").unbind();
	$("#delete-post-form").submit(function(e) {
		var data = $('#delete-post-form').serialize();		// post_id, body
		var url = mf.subfolder + "/microfeed/posts/delete";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var postId = json.postId;
			$('#post-block-'+postId).replaceWith('<div class="alert alert-dismissible alert-warning"><button type="button" class="close" data-dismiss="alert">&times;</button>Post successfully deleted.</div>');
			$('#delete-post-modal').modal('hide');
			//mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$("#show-more-posts-btn").unbind();
	$('#show-more-posts-btn').click(function() {
		mf.loadPosts();
	});

}

////////////////////////////////////////////

mf.loadPosts = function() {
	var data = {
		uid: mf.uid,
		last_post_id: mf.lastPostId,
		post_count: mf.postCount,
		thread: mf.thread,
	}
	var url = mf.subfolder + "/microfeed/ajax/posts";
	$.ajax({
		url: url,
		data: data,
		type: "GET",
		dataType : "json"
	}).done(function( json ) {
		console.log(json);
		for (var i=0; i<json.length; i++) {
			//var args = json[i];  //postId, uid, username, userImage, body, comments, images
			//console.log(json[i].images)
			//args.currentUid = mf.uid;
			mf.displayPost(json[i], 'bottom');		
		}
		$('#show-more-posts-block').remove();
		if (json.length == mf.postCount) {
			if (mf.showMoreOption) {
				var result = mf.templateEngine('more-posts-template', {});
				$('#output').append(result);
			}
			mf.lastPostId = json[mf.postCount-1].postId;
		}
		mf.appendEvents();
	}).fail(function( xhr, status, errorThrown ) {
		$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
		console.log( "Error: " + errorThrown );
		console.log( "Status: " + status );
		console.dir( xhr );
	});
}


////////////////////////////////////////////////

$( document ).ready(function() {
	
	mf.uid = $('#microfeed-container').attr('data-user');
	mf.thread = $('#microfeed-container').attr('data-thread');
	mf.allowComments = ( $('#microfeed-container').attr('data-allow-comments') === "yes" );
	mf.allowComplexPosts = ( $('#microfeed-form').attr('data-allow-complex-post-types') === "yes" );
	mf.allowImages = ( $('#microfeed-form').attr('data-allow-images') === "yes" );

	//load main container
	args = {
		uid: mf.uid
	}
	if (mf.allowComplexPosts) {
		var result = mf.templateEngine('main-form-template', args);
	} else {
		var result = mf.templateEngine('main-form-basic-template', args);
	}
	$('#microfeed-form').html(result);
	var result = mf.templateEngine('main-container-template', args);
	$('#microfeed-container').html(result);
	// show the post form if the user is logged in
	if (mf.uid != 0 && mf.addPostOption) {
		var result = mf.templateEngine('post-form-template', args);
		$('#post-form-block').html(result);
	} else if (mf.addPostOption) {
		var result = mf.templateEngine('post-form-login-template', args);
		$('#post-form-block').html(result);
	}
	if ( mf.allowImages ) {
		var result = mf.templateEngine('open-image-modal-button-template', args);
		$('#new-post-btn').before(result);
	}
	
	//load modals
	args = {}
	var result = mf.templateEngine('modals-template', args);
	$('#microfeed-modals').html(result);
		
	//load first set of posts
	mf.loadPosts();
	
	//configure CROPIT
    $('.image-editor').cropit({
    	exportZoom : 2,
    	maxZoom : 1,
    	minZoom : 'fit',
    	smallImage : 'allow'
    });
    $('.rotate-cw').click(function() {
    	$('.image-editor').cropit('rotateCW');
    });
    $('.rotate-ccw').click(function() {
		$('.image-editor').cropit('rotateCCW');
    });
    $('.export').click(function() {
    	var imageData = $('.image-editor').cropit('export');
    	window.open(imageData);
    });
    
    $('.show-post-form').click(function() {
    	// highlight this button
    	$('.show-post-form').parent().removeClass('active');
    	$(this).parent().addClass('active');
    	//show form
    	var newPlaceholder = $(this).attr('data-placeholder');
    	var currentPlaceholder = $('#new-post-form-body').attr('placeholder');
    	var displayed = $('#post-form-block:visible').length != 0;
    	if ( newPlaceholder == currentPlaceholder && displayed ) {
    		$('#post-form-block').slideUp();
    		$(this).parent().removeClass('active');
    	} else {
    		$('#post-form-block').slideDown();	
        	$('#new-post-form-body').attr('placeholder',newPlaceholder);
    	}
    	return false;
    	
    });
    
    $('.hide-post-form').click(function() {
    	$('#post-form-block').slideUp();
    	return false;
    });

});















