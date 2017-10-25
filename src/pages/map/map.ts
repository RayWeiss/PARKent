import { Component, ViewChild, ElementRef } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { DbRestServiceProvider } from '../../providers/db-rest-service/db-rest-service';
import {} from '@types/googlemaps';
import { Observable } from 'rxjs/Rx';




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
  markers = new Map<string, google.maps.Marker>();
  green = "00CC00";
  yellow = "FFFF00";
  red = "FF0000";
  gray = "808080";
  black = "000000";

  constructor(public navCtrl: NavController, public navParams: NavParams, public dbService: DbRestServiceProvider) {
    this.db = dbService;
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad MapPage');
    this.initMap();
    this.initializeMarkers();
    this.continuallyUpdateMarkers();
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
    .then(spots => {
      // this.spots = data;
      for (var key in spots) {
        var spot = spots[key]
        var name = spot[0];
        // var totalSpots = spot[1];
        var lat = parseFloat(spot[2]);
        var lon = parseFloat(spot[3]);
        // var url = spot[4];

        var marker = new google.maps.Marker({
          position: {lat: lat, lng: lon},
          map: this.map
        });
        marker.setIcon(this.getPinWithHexColor(this.gray));
        var markerAsMarkerObject = marker as google.maps.Marker;
        this.markers.set(name, markerAsMarkerObject);
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

  continuallyUpdateMarkers() {
    const seconds = 5;
    const interval = Observable.interval(seconds * 1000);
    const forever = interval.filter(val => false);

    interval.takeUntil(forever).subscribe(val => {
      var allSpots = [];
      var allStatus = [];
      this.db.getSpots()
      .then(spots => {
        for (var key in spots) {
          var spot = spots[key]
          var name = spot[0];
          allSpots.push(name);
        }
      }).then(spots => {
        for(var spot in allSpots){
          var name = allSpots[spot];

          this.db.getStatus(name)
          .then(status => {
            for (var key in status) {
              var currentStatus = status[key]
              var percentLeft = Number(currentStatus[0]);
              allStatus.push(percentLeft);
            }
            if(allStatus.length == allSpots.length){
              for(var i = 0; i < allSpots.length; ++i) {
                var nameToUpdate = allSpots[i];
                var percentToUpdateWith = allStatus[i];

                var color;

                if(percentToUpdateWith > 0.25) {
                  color = this.green;
                } else if (percentToUpdateWith > 0.10) {
                  color = this.yellow;
                } else if (percentToUpdateWith > 0.0) {
                  color = this.red;
                } else {
                  color = this.black;
                }

                this.markers.get(nameToUpdate).setIcon(this.getPinWithHexColor(color));
              }
              allSpots = [];
              allStatus = [];
            }
          });
        }
      });
    });
  }
}
