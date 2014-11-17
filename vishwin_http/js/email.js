var proto="mailto:";
var handle="vishwin";
var name="charlie";
var name2="c.li";
var info="@vishwin.info";
var state="@psu.edu";

document.getElementsByClassName("pmail")[0].setAttribute("href", proto+handle+info);
document.getElementsByClassName("bmail")[0].setAttribute("href", proto+name+info);
document.getElementsByClassName("amail")[0].setAttribute("href", proto+name2+state);
