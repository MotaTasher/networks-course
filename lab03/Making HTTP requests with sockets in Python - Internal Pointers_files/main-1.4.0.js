var IP;(IP=IP||{}).CONSTS={API:{BASE_URL:"/cms/engine/main.php"},FACEBOOK_PAGE_URL:"https://www.facebook.com/internalpointers/"},(IP=IP||{}).utils={openPopup:function(e,o,t,i){var n=",width="+o+",height="+t+",top="+($(window).height()-t)/2+",left="+($(window).width()-o)/2,s=window.open(e,i,n);window.focus&&s.focus()},sendAnalytics:function(e,o){gtag("event",e,{description:o})},apiCall:function(e,o,t,i){$.ajax({type:"POST",contentType:"application/json",data:JSON.stringify(e),url:IP.CONSTS.API.BASE_URL}).done(function(e,t,i){o(e)}).fail(function(e,o,i){t(i)}).always(function(){i()})},injectScript:function(e,o,t,i){let n=document.getElementById(o);n?n&&i&&i():((n=document.createElement("script")).src=e,n.id=o,n.onload=function(){t&&t()},document.body.appendChild(n))}},$(document).ready(function(){void 0!==Cookies.get("ip-cookie-policy-2018")?$(".ip-cookie-banner").hide():$(".ip-cookie-banner").show(),$(".ip-cookie-banner__close").click(function(e){e.preventDefault(),Cookies.set("ip-cookie-policy-2018",!0,{expires:365}),$(".ip-cookie-banner").hide()})}),(IP=IP||{}).FollowUsPopup={elems:{popup:$(".ip-follow-us-popup"),popupOk:$(".ip-follow-us-popup__body__ok, .ip-follow-us-popup__side, .ip-follow-us-popup__header"),popupNope:$(".ip-follow-us-popup__footer__nope")},vars:{cookieName:"ip-facebook-like",cookieTimeOk:60,cookieTimeKo:14,fadeTime:400,showupTime:15e3},init:function(){if(this.hasCookieExpired()){var e=this;this.elems.popupNope.click(function(o){e.close(o,e.vars.cookieTimeKo,"no facebook like, thanks")}),this.elems.popupOk.click(function(o){e.bindSubscribeEvent()}),window.setTimeout(function(){e.toggle()},e.vars.showupTime)}else this.elems.popup.hide()},toggle:function(){this.elems.popup.fadeToggle(this.vars.fadeTime)},hasCookieExpired:function(){return void 0===Cookies.get(this.vars.cookieName)},bindSubscribeEvent:function(){Cookies.set(this.vars.cookieName,!0,{expires:this.vars.cookieTimeOK}),IP.utils.sendAnalytics("click","facebook like"),window.open(IP.CONSTS.FACEBOOK_PAGE_URL,"_blank"),this.toggle()},close:function(e,o,t){e.preventDefault(),Cookies.set(this.vars.cookieName,!0,{expires:o}),IP.utils.sendAnalytics("click",t),this.toggle()}},$(document).ready(function(){IP.FollowUsPopup.init()}),(IP=IP||{}).Comments={elems:{author:document.querySelector(".ip-post__comments__add input"),body:document.querySelector(".ip-post__comments__add textarea"),form:document.querySelector(".ip-post__comments__add form"),button:document.querySelector(".ip-post__comments__add button"),btnText:document.querySelector(".ip-post__comments__add form button span.text"),btnSpinner:document.querySelector(".ip-post__comments__add form button span.spinner")},init:function(){let e=this;e.elems.form.addEventListener("submit",function(o){o.preventDefault(),IP.utils.injectScript("https://www.google.com/recaptcha/api.js","google-recaptcha",function(){},function(){e.submit()})})},enableSubmit:function(){self.elems.button.disabled=!1},submit:function(){let e=this,o=grecaptcha.getResponse();""!==o?(e.toggleSpinner(),IP.utils.apiCall({route:"api",entity:"comment",action:"insert",data:{idPost:e.elems.form.dataset.idPost,author:e.elems.author.value,body:e.elems.body.value,recaptcha:o}},function(o){e.success(o)},function(o){e.error(o)},function(){grecaptcha.reset(),e.toggleSpinner()})):alert("Please make sure you are not a robot.")},success:function(e){1===e.code?(this.elems.author.value="",this.elems.body.value="",alert("Thanks! Your comment will be visible after approval.")):this.error(e)},error:function(e){alert("Ops! Something went wrong. Please try again...")},toggleSpinner:function(){this.toggle(this.elems.btnText,"inline"),this.toggle(this.elems.btnSpinner)},toggle:function(e,o="block"){e.style.display=window.getComputedStyle(e).display===o?"none":o}},document.addEventListener("DOMContentLoaded",function(){IP.Comments.init()}),document.addEventListener("DOMContentLoaded",function(){let e=window.location.href,o=encodeURIComponent(e),t=encodeURIComponent(document.title);document.querySelector(".ip-post__social-tools__twitter").addEventListener("click",function(i){i.preventDefault();let n="https://twitter.com/share?url="+o+"&text="+t;IP.utils.openPopup(n,575,400,"twitter_popup"),IP.utils.sendAnalytics("click","twitter share of "+e)})});