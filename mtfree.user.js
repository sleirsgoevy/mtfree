// ==UserScript==
// @name        MT_FREE
// @namespace   auto@auth.wi-fi.ru
// @description Automatically authenticate user on MT_FREE
// @include     *
// @version     1
// @grant       none
// ==/UserScript==

var scriptElem = document.createElement('script');
scriptElem.innerHTML = "("+(function()
{
  if((document.location.host == "wi-fi.ru" || document.location.host.indexOf("wi-fi") < 0) && document.title != "Web Authentication Redirect")
    document.location.href = 'http://127.0.0.1:1320/';
  else if(document.location.host == "auth.wi-fi.ru")
  {
    var prev_state = -1;
    var tries = 0;
    var max_tries = 30;
    setInterval(function()
    {
      if(tries >= max_tries)return;
      var state = prev_state;
      var connectBtn = document.querySelector('div.c-branding-button');
      console.log("connectBtn");
      console.log(connectBtn);
      if(connectBtn != null)
      {
        connectBtn.click();
        state = 0;
      }
      else
      {
        var closeBtn = document.querySelector('.mt-banner-fullscreen__button-close');
        console.log("closeBtn");
        console.log(closeBtn);
        if(closeBtn != null)
        {
          closeBtn.click();
          state = 2;
        }
        else
        {
          var banner = document.querySelector('div.content');
          console.log("banner");
          console.log(banner);
          if(banner != null)
          {
            var videos = banner.getElementsByTagName('video');
            console.log("videos");
            console.log(videos);
            for(var i = 0; i < videos.length(); i++)
                videos[i].click();
            state = 1;
          }
          else
          {
            var nextBtn = document.querySelector('div.interaction_button');
            if(nextBtn != null)
            {
              state = 3;
              nextBtn.click();
            }
          }
        }
      }
      if(state <= prev_state)
        tries++;
      else
        tries = 1;
      //if(tries == max_tries)
        //window.close();
    }, 1500);
  }
}).toString()+")()";
document.body.appendChild(scriptElem);
