// ==UserScript==
// @name     MT_FREE
// @version  1
// @grant    none
// @include  *
// ==/UserScript==

var interesting_nodes = ['title', 'div.c-branding-button:nth-child(2)', 'div.c-video-layer:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > video:nth-child(1)', '.interaction_button'];

setInterval(function()
{
  var ans = {'url': document.location.href};
  for(var i = 0; i < interesting_nodes.length; i++)
  {
    var it = document.querySelector(interesting_nodes[i]);
    if(it !== null)
    {
      var rect = it.getBoundingClientRect();
      ans[interesting_nodes[i]] = [rect.left, rect.top, rect.width, rect.height, it.outerHTML];
    }
  }
  console.log(JSON.stringify(ans));
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:4747", true);
  xhr.send(JSON.stringify(ans));
}, 500);
