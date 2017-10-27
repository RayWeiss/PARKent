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
    this.getLotNames();
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ListPage');
  }

  itemSelected(item) {
    this.navCtrl.push('DetailPage', {
      item: item
    });
  }

  getLotNames() {
    this.db.getSpots()
    .then(spots => {
      for (var key in spots) {
        var spot = spots[key]
        var lotName = spot[0];
        var totalSpots = spot[1];
        this.items.push({
          lotName: lotName,
          totalSpots: totalSpots
        });
      }
    });
  }

}
