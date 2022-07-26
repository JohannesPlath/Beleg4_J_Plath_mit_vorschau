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
const SHOULD_PRINT = true;


async function get_image(fname) {
  actualWsi = fname;
  await getNewRegion("init");
}

async function getThumbnail(fname){
    let actualUrl = "./api/thumbnail/" + fname;
    //console.log("-->> @GetThumnail()  actulalURL : " ,  actualUrl);
    document.getElementById("thumbnail").src = actualUrl;
}

async function getLabel(){
    let actualURL = "./api/label/" + actualWsi;
    let label = actualURL
    //console.log("label", label)
    document.getElementById("label").src = actualURL
}

async function getMeta() {
    console.log(" -------------------  >    @ getMeta() Arrived!!!")
    let actualURL = "./api/meta/" + actualWsi;
    meta = await fetch(actualURL)
    let jsonMeta = JSON.parse(await meta.text())
    //console.log("jsonMeta.wsi_meta ", jsonMeta.wsi_meta[0]["openslide.level-count"])
    metaData = jsonMeta.wsi_meta[0]
    setLocalMetaData(jsonMeta.wsi_meta[0]["openslide.level-count"] -1)
}

function setLocalMetaData( currentZoomlevel){
    //console.log("@ setMetaData: ")
    maxHeight =parseInt( metaData["openslide.level[" + 0 + "].height"]);
    maxWidth =  parseInt(metaData["openslide.level[" + 0 + "].width"]);
    actualYLocation = parseInt(metaData["openslide.level[" + currentZoomlevel + "].height"]);
    actualXLocation =  parseInt(metaData["openslide.level[" + currentZoomlevel + "].width"]);
    maxActualHeight = parseInt(metaData["openslide.level[" + currentZoomlevel + "].height"]);
    maxActualWidth =  parseInt(metaData["openslide.level[" + currentZoomlevel + "].width"]);
    //console.log("@ setMetaData + maxWidth: ", maxWidth)
    let maxZoomLevel = parseInt(metaData["openslide.level-count"]);
    // console.log("maxZoomLevel maxZoomLevel , MAXLevelReducer ", maxZoomLevel , MAXLevelReducer)
    actualMaxZoomLevel = maxZoomLevel + MAXLevelReducer

}

async function getListOfImages() {
    let imagelist = await fetch("/api/images");
    //console.log("image list" , imagelist);
    let files = await imagelist.json();
    let filesHtml = "";
    for (i = 0; i < files["images"].length; i++) {
    // console.log(files["images"][i])
        filesHtml = filesHtml + "<a onclick='get_image(\"" + files["images"][i] + "\")'>" + files["images"][i] + "</a><br>";
    }
    document.getElementById("image-selection").innerHTML = filesHtml;
}


async function getThumbnailDetail(fname){
    if ((actualXLocation == NaN)){
        actualXLocation = 100;
        console.log(" ------------actualXLocation == NaN)  ")
        getMeta();
        }
    if ((actualYLocation == NaN)){
        actualYLocation = 100;
        console.log(" ------------actualYLocation == NaN)  ")
        getMeta();
        }
    let xLoc = (actualXLocation / maxActualWidth).toFixed(3)
    let yLoc = (actualYLocation / maxActualHeight).toFixed(3)
    let markedWidth = (shownWidth / maxActualWidth).toFixed(3)
    let markedHeight = (shownHeight / maxActualHeight).toFixed(3)
    let actualUrl = "/api/thumb_detail" +"/"+ fname +"/"+ xLoc+"/"+ yLoc +"/"+ markedWidth +"/"+ markedHeight +"/"+ zoomlevel;
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
        if (actualYLocation <= 0) {
            actualYLocation = 0
        }else if (shownHeight <= maxActualHeight/ Move_FACTOR){
            actualYLocation = actualYLocation - shownHeight;
        }
        else{
            actualYLocation = actualYLocation - maxActualHeight/ Move_FACTOR;
        }
    }
    if (newDetail == "down"){
        if (shownHeight <= maxActualHeight/ Move_FACTOR) {
            actualYLocation = actualYLocation + shownHeight
        }else if ((actualYLocation + shownHeight) > maxActualHeight) {
            actualYLocation = maxActualHeight - shownHeight;
        }else{
            actualYLocation = actualYLocation + maxActualHeight/ Move_FACTOR;
        }

    }
    if (newDetail == "left") {
        if (shownWidth <= maxActualWidth / Move_FACTOR){
            actualXLocation = actualXLocation - shownWidth;
        }else {
            actualXLocation = actualXLocation - maxActualWidth / Move_FACTOR;
            }
        }
    if (newDetail == "right"){
        if (shownWidth <= maxActualWidth / Move_FACTOR){
            actualXLocation = actualXLocation + shownWidth;
        }else {
            actualXLocation = actualXLocation + maxActualWidth / Move_FACTOR;
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

    let actualUrl = "./api/images/" + actualWsi +"/placeholder/" +  Math.floor((actualXLocation)) +"/" +  Math.floor(actualYLocation) + "/" +   shownWidth + "/" + shownHeight + "/" + zoomlevel;
    if (SHOULD_PRINT)
        console.log("func.js getNewRegion",  actualUrl)
    document.getElementById("region-image").src = actualUrl;
}


// helper

function setMaxActualMetaData(currentZoomlevel){
        maxHeight =parseInt( metaData["openslide.level[" + 0 + "].height"]);
        maxWidth =  parseInt(metaData["openslide.level[" + 0 + "].width"]);
        maxActualHeight = parseInt(metaData["openslide.level[" + currentZoomlevel + "].height"]);
        maxActualWidth =  parseInt(metaData["openslide.level[" + currentZoomlevel + "].width"]);

}

function center_View() {
    actualXLocation = maxActualWidth / 2;
    actualXLocation = actualXLocation - (shownWidth / 2);
    if (actualXLocation < 0)
        actualXLocation = 0;
    actualYLocation = maxActualHeight / 2;
    actualYLocation = actualYLocation - (shownHeight / 2);
    if (actualYLocation < 0)
        actualYLocation = 0;
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
    if (actualXLocation > maxActualWidth - shownWidth){
        actualXLocation = maxActualWidth - shownWidth;
       /* if (actualXLocation > maxActualWidth){
            actualXLocation = maxActualWidth;
        }*/
    }
    if (actualXLocation < 0)
        actualXLocation = 0;
    return actualXLocation;
}
function checkHeightExtrema(){

    if (actualYLocation > maxActualHeight - shownHeight)
        actualYLocation = maxActualHeight - shownHeight;
    if (actualYLocation < 0 )
        actualYLocation = 0;
    return actualYLocation;
}

function checkActualZoomLevel(){
    if (zoomlevel > actualMaxZoomLevel)
        zoomlevel = actualMaxZoomLevel
    if (zoomlevel < 0)
            zoomlevel =0
    return zoomlevel
}