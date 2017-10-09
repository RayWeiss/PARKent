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

  constructor(public navCtrl: NavController, public navParams: NavParams, public dbService: DbRestServiceProvider) {
    this.db = dbService;
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad MapPage');
    this.initMap();
  }

  initMap() {
    this.map = new google.maps.Map(this.mapElement.nativeElement, {
      zoom: 16,
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

}
