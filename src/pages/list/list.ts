import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { DbRestServiceProvider } from '../../providers/db-rest-service/db-rest-service';

@IonicPage()
@Component({
  selector: 'page-list',
  templateUrl: 'list.html',
  providers: [DbRestServiceProvider]
})
export class ListPage {
  items: any[];
  db: any;

  constructor(public navCtrl: NavController, public navParams: NavParams, public dbService: DbRestServiceProvider) {
    this.db = dbService;
    this.items = [];
    this.getFracLeft();
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ListPage');
  }

  itemSelected(item) {
    this.navCtrl.push('DetailPage', {
      item: item
    });
  }

  getFracLeft() {
    this.db.getFracLeft()
    .then(response => {
      for (var val in response) {
        var spots = response[val];
        for (var spot in spots) {
          var lotName = spot;
          var fracValues = spots[spot];
          var spotsLeft = fracValues[0];
          var totalSpots = fracValues[1];
          this.items.push({
            lotName: lotName,
            spotsLeft: spotsLeft,
            totalSpots: totalSpots
          });
        }
      }
    });
  }

}
