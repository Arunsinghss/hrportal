$(document).ready(function(){

	$ns = $('.ns-administrator-wrapper')
	$('.tabs').tabs();
	$('.modal').modal();
	$('select').formSelect();
	$('div.row.signup').hide();
	$('.datepicker').datepicker();
	$('.collapsible').collapsible();
	$('input#input_text, textarea#textarea2').characterCounter();


	var login = function() {

		$('#slogin').click(function(){
			$('div.row.signup').hide();
			$('div.row.login').show();
		});
	}

	var showmodal = function() {

		$('.chatbutton').click(function(){
			$(this).css({"color":"#ee6e73"})
			$id = $(this).attr("id")
			$('.modal.'+$id).modal('open');
		});

		$('.policycommentbutton').click(function(event){
			$(this).css({"color":"#ee6e73"})
			event.stopPropagation();
			$id = $(this).attr("id")
			$('.policymodal.'+$id).modal('open');
		});
	}

	var like = function(){

		$('.likebutton').click(function(event){

			$(this).css({"color":"#ee6e73"})
			event.preventDefault();
			$aid = $(this).attr('id');
			$tab = $(this).attr('tab');
			$element = $(this).parent().children('.like');
			$count = parseInt($element.text()) + 1 

			$.ajax({
				type : "POST",
				url : "/portal/like",
				datatype : "json",
				data : {
					"csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
					"aid" : $aid,
					"tab" : $tab
				},	
				success : function(data){
					if (data.success){
						M.toast({html:"Liked Successfully"},"#ee6e73")
						$element.text(parseInt($element.text()) + 1)
					}
					else{
						M.toast({html: data.message})	
					}
				}
			});
		});
	}

	var deletefile = function() {

		$('.deletebutton').click(function(event){
			event.preventDefault();
			$(this).css({"color":"#ee6e73"})
			$fid = $(this).attr('id');
			$tab = $(this).attr('tab')

			$.ajax({
				type : "POST",
				url : "/portal/delete",
				datatype : "json",
				data : {
					"csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
					"fid" : $fid,
					"tab" : $tab
				},	
				success : function(data){
					if (data.success){
						M.toast({html:"File deleted Successfully"})
						$("."+$fid).remove();
					}
					else{
						M.toast({html: data.message})	
					}
				}
			});
		});
	}

	var markresolve = function() {

		$('.resolve').click(function(event){
			event.stopPropagation();
			$element = $(this)
			$qid = $(this).attr('id');

			$.ajax({
				type : "POST",
				url : "/portal/resolve",
				datatype : "json",
				data : {
					"csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
					"qid" : $qid,
				},	
				success : function(data){
					if (data.success){
						M.toast({html:"Marked Resolved"});
						$element.css({"color":"#ee6e73"});
					}
					else{
						M.toast({html: "Something wrong happened"})	
					}
				}
			});
		});
	}

	var answer = function() {

		$('.answer').click(function(event){
			$element = $(this)
			$qid = $(this).attr('id');
			$replybox = $(this).parent().children('.input-field').children('.replybox')
			$text = $replybox.val();

			$.ajax({
				type : "POST",
				url : "/portal/addanswer",
				datatype : "json",
				data : {
					"csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
					"qid" : $qid,
					"reply": $text
				},	
				success : function(data){
					if (data.success){
						M.toast({html:"Replied Successfully"});
						$element.parent().siblings('.bodyanswer').append(data.newreply);
						$replybox.val("")
					}
					else{
						M.toast({html: "Something wrong happened"})	
					}
				}
			});
		});
	}

	var comment = function() {

		$('.commentbutton').click(function(event){
			
			event.preventDefault();
			var $pid;
			$aid = $(this).attr('answerid');
			$chatfield = $('label.comment.'+$aid)
			$chatcount = parseInt($chatfield.text())+1
			$text = $('.commentbox.'+$aid).val()
			$list = $(this).parent('.row.commentfeed').siblings('.commentlist')

			$.ajax({
				type : "POST",
				url : "/portal/comment",
				datatype : "json",
				data : {
					"csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
					"aid" : $aid,
					"$pid": $pid,
					"comment" : $text
				},	
				success : function(data){
					if (data.success){
						M.toast({html:"Comment Successfull"})
						$list.append(data.comment);
						$chatfield.text($chatcount);
						$('.modal.'+$aid).modal('close');
					}
					else{
						M.toast({html: "something wrong happened"})	
					}
				}
			});
		});

		$('.policycomment').click(function(event){
			
			event.preventDefault();
			var $aid;
			$pid = $(this).attr('policyid');
			$text = $('.commentbox.'+$pid).val()
			$chatfield = $('label.policycomment.'+$pid)
			$chatcount = parseInt($chatfield.text())+1
			$list = $(this).parent('.row.commentfeed').siblings('.commentlist')

			$.ajax({
				type : "POST",
				url : "/portal/comment",
				datatype : "json",
				data : {
					"csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
					"aid" : $aid,
					"pid":$pid,
					"comment" : $text
				},	
				success : function(data){
					if (data.success){
						M.toast({html:"Comment Successfull"})
						$list.append(data.comment);
						$chatfield.text($chatcount);
						$('.policymodal.'+$pid).modal('close');
					}
					else{
						M.toast({html: "something wrong happened"})	
					}
				}
			});
		});
	}

	like();
	login();
	answer();
	comment();
	showmodal();
	deletefile();
	markresolve();
});




	// $('#signup').click(function(){
	// 	$('div.row.login').hide();
	// 	$('div.row.signup').show();
	// })


	// $('#successlogin').click(function(){
	// 	window.location.href = 'login';
	// 	$('div.row.signup').hide();
	// 	$('div.row.login').show();
	// })
