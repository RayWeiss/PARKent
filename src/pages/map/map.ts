import { Component, ViewChild, ElementRef } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { DbRestServiceProvider } from '../../providers/db-rest-service/db-rest-service';

declare var google;

@IonicPage()
@Component({
  selector: 'page-map',
  templateUrl: 'map.html',
  providers: [DbRestServiceProvider]
})
export class MapPage {

  @ViewChild('map') mapElement: ElementRef;
  map: any;
  db: any;
  markers = {};
  spots: any;

  green = "00CC00";
  yellow = "FFFF00";
  red = "FF0000";

  constructor(public navCtrl: NavController, public navParams: NavParams, public dbService: DbRestServiceProvider) {
    this.db = dbService;
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad MapPage');
    this.initMap();
    this.initializeMarkers();
  }

  initMap() {
    this.map = new google.maps.Map(this.mapElement.nativeElement, {
      zoom: 15,
      center: {lat: 41.147799193274636, lng: -81.34373903024539},
      streetViewControl: false,
      mapTypeControl: false,
      clickableIcons: false,
    });
    this.map.setOptions({styles: [
      {
        featureType: 'poi',
        stylers: [{visibility: 'off'}]
      }
    ]});
  }

  initializeMarkers() {
    this.db.getSpots()
    .then(data => {
      this.spots = data;
      for (var key in this.spots) {
        var spot = this.spots[key]
        var name = spot[0];
        var totalSpots = spot[1];
        var lat = parseFloat(spot[2]);
        var lon = parseFloat(spot[3]);
        var url = spot[4];

        var marker = new google.maps.Marker({
          position: {lat: lat, lng: lon},
          map: this.map
        });
        marker.setIcon(this.getPinWithHexColor(this.red));
        // marker.setIcon(this.getCircleWithHexColor(this.green));
        this.markers[name] = marker;
      }
    });
  }

  getPinWithHexColor(color) {
    return new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + color,
      new google.maps.Size(21, 34),
      new google.maps.Point(0,0),
      new google.maps.Point(10, 34));
  }

  getCircleWithHexColor(color) {
    return {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 10.0,
        fillColor: "#" + color,
        fillOpacity: 1.0,
        strokeWeight: 0.0
    }
  }

  changeLotMarkerToColor(lotName, color) {
    // this.markers[lotName].setIcon(this.getPinWithHexColor(color));
  }
}
