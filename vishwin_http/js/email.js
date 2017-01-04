/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var proto="mailto:";
var handle="vishwin";
var name="charlie";
var name2="c.li";
var git="git";
var info="@vishwin.info";
var state="@psu.edu";

document.getElementsByClassName("pmail")[0].setAttribute("href", proto+handle+info);
document.getElementsByClassName("bmail")[0].setAttribute("href", proto+name+info);
document.getElementsByClassName("amail")[0].setAttribute("href", proto+name2+state);
document.getElementsByClassName("patchmail")[0].setAttribute("href", proto+git+info);
