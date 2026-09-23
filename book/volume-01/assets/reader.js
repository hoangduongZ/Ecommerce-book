
const btn=document.querySelector('.menu-btn'), side=document.querySelector('.sidebar');
function closeNav(){side?.classList.remove('open');document.body.classList.remove('nav-open')}
btn?.addEventListener('click',()=>{side?.classList.toggle('open');document.body.classList.toggle('nav-open')});
document.addEventListener('click',e=>{if(document.body.classList.contains('nav-open')&&!side.contains(e.target)&&e.target!==btn)closeNav()});
document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',closeNav));
