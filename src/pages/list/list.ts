import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';

@IonicPage()
@Component({
  selector: 'page-list',
  templateUrl: 'list.html',
})
export class ListPage {
  items: any[];

  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.items = [];
    for(let i = 0; i < 10; ++i) {
      this.items.push({
        text: 'Item ' + i,
        id: i
      });
    }
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ListPage');
  }

  itemSelected(item) {
    this.navCtrl.push('DetailPage', {
      item: item
    });
  }

}
