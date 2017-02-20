	mf2 = {}
	

	mf2.postCount = 10;
	mf2.lastPostId = 1000000;
	mf2.threadId = 1;
	mf2.postIdToDelete = 0;
	
	mf2.loadFeed = function() {
		var data = {
			last_post_id: mf2.lastPostId,
			post_count: mf2.postCount,
			thread_id: mf2.threadId
		}
		$.ajax({
			url: "/microfeed2/ajax/posts",
			type: "GET",
			dataType : "json",
			data : data
		})
		.done(function( json ) {
			$('#mf-load-more-posts-btn').replaceWith('');
			$('#mf-feed').append(json.html);
			$('body').append(json.modals);
			crp.load();
			mf2.attachEvents();
			if ( json.status == 'unfinished' ) {
				mf2.lastPostId = json.lastPostId;
			} else {
				$('#mf-load-more-posts-btn').replaceWith('');
			}
				
			$('#mf-load-more-posts-btn').click(function() {
				mf2.loadFeed();
			});
			$('#mf-confirm-delete-post-btn').click(function() {
				$.ajax({
					url: "/microfeed2/posts/delete/" + mf2.postIdToDelete,
					type: "POST",
					dataType : "json",
					data : {dummy : 'nothing'}
				})
				.done(function( json ) {
					$('#' + json.destinationId).replaceWith(json.html);
				})
				.fail(function( xhr, status, errorThrown ) {
					alert( "error" );
					console.log( "Error: " + errorThrown );
					console.log( "Status: " + status );
					console.dir( xhr );
				});
				$('#mf-delete-post-modal').modal('hide');
			});
		})
		.fail(function( xhr, status, errorThrown ) {
			alert( "error" );
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});
	}
	
	mf2.attachEvents = function () {
		$('.mf-new-post-form').unbind().submit(function(event) {
			event.preventDefault();
			$.ajax({
				url: "/microfeed2/posts/new",
				type: "POST",
				dataType : "json",
				data : $(this).serialize()
			})
			.done(function( json ) {
				if ( json.status == 'OK' ) {
					$('#mf-feed').prepend(json.html);
				}
				else {
					$('#mf-event').html(json.html);
				}
				// $('.mf-new-post-form').find("input[type=text], textarea").val("");
				$('.mf-new-post-form').trigger('reset');
				mf2.attachEvents();
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			});
		});
		$('.mf-edit-post-form').unbind().submit(function(event) {
			var postId = $(this).attr('data-post-id');
			event.preventDefault();
			$.ajax({
				url: "/microfeed2/posts/edit/" + postId,
				type: "POST",
				dataType : "json",
				data : $(this).serialize()
			})
			.done(function( json ) {
				if (json.status == 'OK') {
					$('#' + json.destinationId).html(json.html);
				} else {
					$('#' + json.destinationId).html(json.html);
				}
				crp.load();
				mf2.attachEvents();
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			});
		});
		$('.mf-edit-post-btn').unbind().click(function() {
			var postId = $(this).attr('data-post-id');
			$.ajax({
				url: "/microfeed2/posts/edit/" + postId,
				type: "GET",
				dataType : "json",
				data : {}
			})
			.done(function( json ) {
				$('#' + json.destinationId).html(json.html);
				crp.load();
				mf2.attachEvents();
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			});
			return false;
		});
		$('.mf-cancel-post-edit').unbind().click(function() {
			var postId = $(this).attr('data-post-id');
			$.ajax({
				url: "/microfeed2/posts/" + postId,
				type: "GET",
				dataType : "json",
				data : {}
			})
			.done(function( json ) {
				$('#' + json.destinationId).html(json.html);
				crp.load();
				mf2.attachEvents();
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			});
			return false;
		});
		$('.mf-edit-comment-btn').unbind().click(function() {
			var commentId = $(this).attr('data-comment-id');
			$('#mf-view-comment-'+commentId).hide();
			$('#mf-edit-comment-'+commentId).show();
			// ajax to load comment form
			$.ajax({
				url: "/microfeed2/ajax/comments/edit/" + commentId,
				type: "GET",
				dataType : "json",
				data: {commentId : commentId}
			})
			.done(function( json ) {
				$('#' + json.destinationId).html(json.html);
				mf2.attachEvents();
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			})
			return false;
		});
		$('.mf-cancel-comment-edit').unbind().click(function() {
			var commentId = $(this).attr('data-comment-id');
			$('#mf-edit-comment-'+commentId).hide();
			$('#mf-view-comment-'+commentId).show();
		});
		$('.mf-edit-comment-form').unbind().submit(function(event) {
			var commentId = $(this).attr('data-comment-id');
			event.preventDefault();
			$.ajax({
				url: "/microfeed2/ajax/comments/edit/" + commentId,
				type: "POST",
				dataType : "json",
				data : $(this).serialize()
			})
			.done(function( json ) {
				$('#' + json.destinationId).html(json.html);
				mf2.attachEvents();
				if (json.status == 'complete') {
					$('#mf-edit-comment-'+commentId).hide();
					$('#mf-view-comment-'+commentId).show();
				}
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			});
		});
		$('.mf-new-comment-form').unbind().submit(function(event) {
			var postId = $(this).attr('data-post-id');
			event.preventDefault();
			$.ajax({
				url: "/microfeed2/ajax/posts/" + postId + "/comments/new",
				type: "POST",
				dataType : "json",
				data : $(this).serialize()
			})
			.done(function( json ) {
				if ( json.status == 'complete' ) {
					$('#mf-post-comment-list-'+json.postId).append(json.html);
					$('#mf-new-comment-form-'+json.postId)[0].reset();
					mf2.attachEvents();
				}
			})
			.fail(function( xhr, status, errorThrown ) {
				alert( "error" );
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
			});
		});
		$('.mf-delete-post-btn').unbind().click(function() {
			var postId = $(this).attr('data-post-id');
			mf2.postIdToDelete = postId;
			$('#mf-delete-post-modal').modal('show');
			return false;
		});
		$('.dateinput').datetimepicker({format: 'll'});
		$('.timeinput').datetimepicker({format: 'hh:mm A'});
	}
	
	
	$(document).ready(function() {
		
		mf2.threadId = $('#mf-feed').attr('data-thread-id');
		mf2.loadFeed();
		
		
		
		$('#mf-post-form-teaser').click(function() {
			$('#mf-post-form-teaser-container').hide();
			$('#mf-post-forms-container').slideDown();
			$('#default-post-form textarea').focus();
		});
		
		$('.mf-show-pill').click(function() {
			var targetId = $(this).attr('data-target-id');
			$('.mf-show-pill').parent().removeClass('active');
			$(this).parent().addClass('active');
			$('.mf-post-form-container').hide();
			$(targetId).fadeIn();
		});
		
		$('#mf-cancel-new-post').click(function() {
			$('#mf-post-forms-container').hide();
			$('#mf-post-form-teaser-container').show();
		});
		
		
		
		
		
	});