/* determine which size of image to load */
function getSize(scaling = 1) {
    var trueRes
    
    var orientation = (screen.orientation || {}).type || screen.mozOrientation || screen.msOrientation;
    if (orientation === "portrait-secondary" || orientation === "portrait-primary")
        trueRes = screen.height / window.devicePixelRatio
    else
        trueRes = screen.width / window.devicePixelRatio
    
    if (scaling != null)
        trueRes = trueRes * scaling
    
    if (trueRes < 640)
        return '?scalex=640&scaley=480'
    if (trueRes < 1024)
        return '?scalex=1024&scaley=768'
    if (trueRes < 1280)
        return '?scalex=1280&scaley=960'
    if (trueRes < 1400)
        return '?scalex=1400&scaley=1050'
    if (trueRes < 1600)
        return '?scalex=1600&scaley=1200'
    if (trueRes < 1920)
        return '?scalex=1920&scaley=1440'
    else
        return '?scalex=4000&scaley=3000'
}

/* check if browser is capable of webp */
function supportsWebp() {
    return /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

    /* alternative to check for webP support */
    //if (!self.createImageBitmap) return false;
    //const webpData = 'data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=';
    //return createImageBitmap(webpData).then(() => true, () => false);
}

/* cache */
var webP = supportsWebp()
var elements = null
var counter = 0

/* garantuee initall call evaluates to true */
var viewbox_y = -Infinity

IDENT = "realsrc"
SCALING = "realscaling"
WIDTH_LOCK = "LAZYLOAD_WIDTH"
HEIGHT_LOCK = "LAZYLOAD_HEIGHT"

/* function to load images */
function changeSrc(offset){

    /* check if there was a relevant change */
    var cur_viewbox = -document.getElementById("top").getBoundingClientRect().y
    if(cur_viewbox - viewbox_y < 100){
        return;

    }

    /* cache viewbox */
    viewbox_y = cur_viewbox

    /* cache */
    if(elements == null){
        elements = document.querySelectorAll("*[" + IDENT + "]");
    }

    for (var i = counter; i < elements.length; i++) {
            var boundingClientRect = elements[i].getBoundingClientRect();
            if (elements[i].hasAttribute(IDENT)
                    && boundingClientRect.top < window.innerHeight + offset) {

                var newSrc = elements[i].getAttribute(IDENT)
                var xWidth  = elements[i].getAttribute(WIDTH_LOCK)
                var yHeight = elements[i].getAttribute(HEIGHT_LOCK)

                /* remove url( ... ) if it is used */
                //newSrc = newSrc.substring(4,newSrc.length-1)

                
                /* determine & set the correct width and height */
                if(xWidth || yHeight){
                    if(xWidth !=null && xHeight != null){
                            newSrc += "?scalex=" + xWidth + "&scaley=" + yHeight
                    }else if(xWdith != null){
                            newSrc += "?x=" + xWidth
                    }else{
                            newSrc += "?y=" + yHeight
                    }
                } else {
                    scaling = elements[i].getAttribute(SCALING)
                    newSrc += getSize(scaling)
                }

                /* load webP if supported */
                if(webP){
                    newSrc = newSrc  + '&encoding=webp'
                }
                
                elements[i].setAttribute("src", newSrc);
                elements[i].style.backgroundImage = 'url(' + newSrc +')';
                elements[i].removeAttribute(IDENT);
            }else{
                /* DOM is parsed top down and images are inserted in that order too */
                /* meaing that once we reach pic that insnt in viewbox none following will be*/
                counter = i;
                return;
            }
        }

    /* if we got here we are done */
    document.getElementById("main_scrollable").removeEventListener("scroll",refresh_handler);

}
var refresh_handler = function(e) {
    /* images directly in view first (offset 0)*/
    //changeSrc(0)
    /* then load images almost in view */
    changeSrc(500)
};

/* add listeners */
document.addEventListener('scroll', refresh_handler);
window.addEventListener('resize', refresh_handler);
window.addEventListener('load', refresh_handler);
getSize()