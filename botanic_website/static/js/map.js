if (typeof BMap === 'undefined') {
  throw new Error('map JavaScript requires BMap')
}

// 创建Map实例地图
var map = new BMap.Map("allmap");
// 设置中心点坐标
var point = new BMap.Point(116.331398, 39.897445);
// 初始化地图
/**
 * 地图类型：
 * 普通地图：BMAP_NORMAL_MAP
 * 卫星地图：BMAP_HYBRID_MAP
 */
var map = new BMap.Map("map", { mapType: BMAP_NORMAL_MAP, minZoom: 1, maxZoom: 18}); // 设置地图类型及最小最大级别
// 设置地图级别（1-18）
map.centerAndZoom(point, 12);
// 开启滚轮缩放地图
map.enableScrollWheelZoom();
// 进行浏览器定位
var geolocation = new BMap.Geolocation();
geolocation.getCurrentPosition(function(r){
    // 定位成功实践
    if(this.getStatus() == BMAP_STATUS_SUCCESS){
        // alert('您的位置：' + r.point.lng, +r.point.lat);
        var point = new BMap.Point(r.point.lng, +r.point.lat);
    }
 },{enableHighAccuracy: true});
// addEventListener--添加事件监听函数
// click--点击事件获取经纬度
map.addEventListener("click", function (e) {
    promise("鼠标单机地方的经纬度为：", e.point.lng + "," + e.point.lat);
});
