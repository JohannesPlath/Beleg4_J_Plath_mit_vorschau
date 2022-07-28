let actualWsi = ""
let shownWidth = 1200;
let shownHeight = 1200;
var actualXLocation ;
var actualYLocation ;
var maxActualWidth ;
var maxActualHeight ;
var zoomlevel = 0 ;
let maxHeight;
let maxWidth;
let actualMaxZoomLevel;
let metaData;
const MAXLevelReducer = -1;
const Move_FACTOR = 5;
const THUMBNAILSIZE = 500;
const SHOULD_PRINT = false;


async function get_image(fname) {
  actualWsi = fname;
  await getNewRegion("init");
}

async function getThumbnail(fname){
    let actualUrl = "./api/wsis/" + fname + "/thumbnail ";
     if (SHOULD_PRINT)
        console.log("-->> @GetThumnail()  actulalURL : " ,  actualUrl);
    document.getElementById("thumbnail").src = actualUrl;
}

async function getLabel(){
    let actualURL = "./api/wsis/" + actualWsi +"/label";
    let label = actualURL
     if (SHOULD_PRINT)
        console.log("label", label)
    document.getElementById("label").src = actualURL
}

async function getMeta() {
    if (SHOULD_PRINT)
        console.log(" -------------------  >    @ getMeta() Arrived!!!")
    let actualURL = "./api/meta/" + actualWsi;
    meta = await fetch(actualURL)
    let jsonMeta = JSON.parse(await meta.text())
    if (SHOULD_PRINT)
        console.log("jsonMeta.wsi_meta ", jsonMeta.wsi_meta[0]["openslide.level-count"])
    metaData = jsonMeta.wsi_meta[0]
    setLocalMetaData(jsonMeta.wsi_meta[0]["openslide.level-count"] -1)
}

function setLocalMetaData( currentZoomlevel){
     if (SHOULD_PRINT)
        console.log("@ setMetaData: ")
    maxHeight =parseInt( metaData["openslide.level[" + 0 + "].height"]);
    maxWidth =  parseInt(metaData["openslide.level[" + 0 + "].width"]);
    actualYLocation = parseInt(metaData["openslide.level[" + currentZoomlevel + "].height"]);
    actualXLocation =  parseInt(metaData["openslide.level[" + currentZoomlevel + "].width"]);
    maxActualHeight = parseInt(metaData["openslide.level[" + currentZoomlevel + "].height"]);
    maxActualWidth =  parseInt(metaData["openslide.level[" + currentZoomlevel + "].width"]);
     if (SHOULD_PRINT)
        console.log("@ setMetaData + maxWidth: ", maxWidth)
    let maxZoomLevel = parseInt(metaData["openslide.level-count"]);
     if (SHOULD_PRINT)
        console.log("maxZoomLevel maxZoomLevel , MAXLevelReducer ", maxZoomLevel , MAXLevelReducer)
    actualMaxZoomLevel = maxZoomLevel + MAXLevelReducer

}

async function getListOfImages() {
    let imagelist = await fetch("/api/wsis");
    //console.log("image list" , imagelist);
    let files = await imagelist.json();
    let filesHtml = "";
    for (i = 0; i < files["images"].length; i++) {
         if (SHOULD_PRINT)
             console.log(files["images"][i])
        filesHtml = filesHtml + "<a onclick='get_image(\"" + files["images"][i] + "\")'>" + files["images"][i] + "</a><br>";
    }
    document.getElementById("image-selection").innerHTML = filesHtml;
}

/**
 * method to set a picture @ "thumbnail"
 * caused by a backend response
 * @param fname
 * @returns {Promise<void>}
 */
async function getThumbnailDetail(fname){
    actualXLocation = checkIsNaN(actualXLocation)
    actualYLocation = checkIsNaN(actualYLocation)
    let xLoc = (actualXLocation / maxWidth).toFixed(3)
    let yLoc = (actualYLocation / maxHeight).toFixed(3)
    let markedWidth = ((shownWidth / maxActualWidth)).toFixed(3)
    let markedHeight = ((shownHeight / maxActualHeight)).toFixed(3)
    let actualUrl = "/api/wsis/"+ fname  + "/thumb_detail/"+ xLoc+"/"+ yLoc +"/"+ markedWidth +"/"+ markedHeight +"/"+ zoomlevel;
    if (SHOULD_PRINT)
        console.log("-->> @GetThumnailDetail()  actulalURL : " ,  actualUrl);

    document.getElementById("thumbnail").src = actualUrl;
}

async function getNewRegion(newDetail){
    if (newDetail == "init"){
        await getMeta();
        //await getThumbnailDetail(actualWsi);
        await getLabel(actualWsi);
        setLocalMetaData(zoomlevel);
        zoomlevel = actualMaxZoomLevel;
        actualYLocation = 1 //actualYLocation / 2;
        actualXLocation = 1// actualXLocation / 2;
        checkActualZoomLevel();
        center_View();

    }

    if (newDetail == "up"){
        if (((shownHeight / maxActualHeight)*maxHeight) < maxHeight/ Move_FACTOR){
            actualYLocation = actualYLocation - ((shownHeight / maxActualHeight)*maxHeight) *0.95;
        }
        else if (shownHeight >= maxHeight / Move_FACTOR){
            actualYLocation = actualYLocation - shownHeight;
        }
        else{
            actualYLocation = actualYLocation - maxHeight/ Move_FACTOR;
        }
    }
    if (newDetail == "down"){
        if (((shownHeight / maxActualHeight)*maxHeight) < maxHeight/ Move_FACTOR){
            actualYLocation = actualYLocation + ((shownHeight / maxActualHeight)*maxHeight) *0.95;
        }
        else if (shownHeight >= maxHeight/ Move_FACTOR) {
            actualYLocation = actualYLocation + shownHeight
        }
        else if ((actualYLocation + shownHeight) > maxHeight) {
            actualYLocation = maxHeight - shownHeight;
        }else{
            actualYLocation = actualYLocation + maxHeight/ Move_FACTOR;
        }

    }
    if (newDetail == "left") {
        if (((shownWidth / maxActualWidth) * maxWidth) < maxWidth/ Move_FACTOR){
            actualXLocation = actualXLocation - ((shownWidth / maxActualWidth) * maxWidth) *0.95;
        }
        else if (shownWidth >= maxWidth / Move_FACTOR){
            actualXLocation = actualXLocation - shownWidth;
        }else {
            actualXLocation = actualXLocation - maxWidth / Move_FACTOR;
            }
        }
    if (newDetail == "right"){
        if (((shownWidth / maxActualWidth) * maxWidth) < maxWidth/ Move_FACTOR){
            actualXLocation = actualXLocation + ((shownWidth / maxActualWidth) * maxWidth) *0.95;
        }
        else if (shownWidth >= maxWidth / Move_FACTOR){
            actualXLocation = actualXLocation + shownWidth;
        }else {
            actualXLocation = actualXLocation + maxWidth / Move_FACTOR;
            }
        }
    if (newDetail == "Zoom_Out"){
        zoomlevel = zoomlevel + 1;
        checkActualZoomLevel();
        setLocalMetaData(zoomlevel);
        center_View();
    }
    if (newDetail == "Zoom_In"){
        zoomlevel = zoomlevel - 1;
        checkActualZoomLevel();
        setLocalMetaData(zoomlevel);
        center_View();
    }
    setMaxActualMetaData(zoomlevel);
    checkHeightExtrema();
    checkWidthExtrema();
    if (SHOULD_PRINT)
        console.log("@ getNewRegion printMetaData()", await printMetadata());
    await getThumbnailDetail(actualWsi);
    await askForImage()
}

async function askForImage(){
    actualXLocation = checkIsNaN(actualXLocation)
    actualYLocation = checkIsNaN(actualYLocation)
    let actualUrl = "./api/wsis/" + actualWsi +"/region/" +  Math.floor((actualXLocation)) +"/" +  Math.floor(actualYLocation) + "/" +   shownWidth + "/" + shownHeight + "/" + zoomlevel;
    if (SHOULD_PRINT)
        console.log("func.js getNewRegion",  actualUrl)
    document.getElementById("region-image").src = actualUrl;
}


// helper

function checkIsNaN(toCheck){
    if (isNaN(toCheck))
        return 1
    else
        return toCheck
}

function setMaxActualMetaData(currentZoomlevel){
        maxHeight =parseInt( metaData["openslide.level[" + 0 + "].height"]);
        maxWidth =  parseInt(metaData["openslide.level[" + 0 + "].width"]);
        maxActualHeight = parseInt(metaData["openslide.level[" + currentZoomlevel + "].height"]);
        maxActualWidth =  parseInt(metaData["openslide.level[" + currentZoomlevel + "].width"]);

}

function center_View() {
    actualXLocation = (maxWidth / 3)  ;
    if (actualXLocation < 0)
        actualXLocation = 1;
    actualYLocation = (maxHeight / 3);
    if (actualYLocation < 0)
        actualYLocation = 1;
    if (SHOULD_PRINT) {
        console.log("@ center_View print...")
        printMetadata()
    }
}

function printMetadata(){
    if (SHOULD_PRINT) {
        console.log("actualXLocation ", actualXLocation);
        console.log("actualYLocation ", actualYLocation);
        console.log("maxActualWidth ", maxActualWidth);
        console.log("maxAtualHeight ", maxActualHeight);
        console.log("zoomlevel ", zoomlevel);
        console.log("maxWidth ", maxWidth);
        console.log("maxHeight ", maxHeight);
        console.log("shown height ", shownHeight)
        console.log("shown width ", shownWidth)
        console.log("actualMaxZoomLevel ", actualMaxZoomLevel);
    }
}
function checkWidthExtrema(){
    if (actualXLocation > maxWidth - shownWidth){
        actualXLocation = maxWidth - shownWidth;
       /* if (actualXLocation > maxActualWidth){
            actualXLocation = maxActualWidth;
        }*/
    }
    if (actualXLocation < 0)
        actualXLocation = 1;
    return actualXLocation;
}
function checkHeightExtrema(){

    if (actualYLocation > maxHeight - shownHeight)
        actualYLocation = maxHeight - shownHeight;
    if (actualYLocation < 0 )
        actualYLocation = 1;
    return actualYLocation;
}

function checkActualZoomLevel(){
    if (zoomlevel > actualMaxZoomLevel)
        zoomlevel = actualMaxZoomLevel
    if (zoomlevel < 0)
            zoomlevel =0
    return zoomlevel
}