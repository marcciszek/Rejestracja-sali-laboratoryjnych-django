  function getShortText(text)
  {
    let visibletext = text.toString().slice(0,30);
      if (text.length>20) visibletext+="[...]";
      return visibletext;
  }

  document.addEventListener('DOMContentLoaded',function(){
    const descs = document.querySelectorAll('.room-description');
    [...descs].forEach((el)=>{
      el.title = el.innerText.toString();
      el.innerText = getShortText(el.innerText.toString());
el.addEventListener('click',function(){
        if (this.innerText.toString()==this.title.toString())
        {
          this.innerText = getShortText(this.title.toString());
        }
        else
        {
          this.innerText = this.title.toString();
        }
      });
    });
  });