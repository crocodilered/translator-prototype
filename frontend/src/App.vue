
<template>
  <ui-grid>
    <ui-grid-cell columns="12">
      <ui-textfield
        v-model="source"
        input-type="textarea"
        fullwidth
        placeholder="HTML"
        maxlength=""
        rows="8"
      ></ui-textfield>
    </ui-grid-cell>
  </ui-grid>
  <ui-grid>
    <ui-grid-cell columns="12"> 
      <ui-select v-model="langFrom" :options="langsFrom"></ui-select>
      &nbsp;
      <ui-select v-model="langTo" :options="langsTo"></ui-select>
      &nbsp;
      <ui-button raised @click="translate">Перевести</ui-button>
    </ui-grid-cell>
  </ui-grid>
  <ui-grid>
    <ui-grid-cell columns="12">
      <ui-card outlined v-show="!loading && result != ''">
        <ui-card-content>
          <ui-card-text>
            <h2>Перевод</h2>
            <div v-html="result"></div>
          </ui-card-text>
        </ui-card-content>
      </ui-card>
      <ui-spinner active :closed="!loading"></ui-spinner>
    </ui-grid-cell>
  </ui-grid>
</template>

<script>
import axios from 'axios';

export default {
    name: 'p-app',

    data () {
      const langsFrom = [
        {value: 'ru_RU', label: 'с русского'},
        {value: 'ky_KG', label: 'с киргизского'},
        {value: 'uz_UZ', label: 'с узбекского'},
        {value: 'tg_TJ', label: 'с таджикского'}
      ]
      const langsTo = [
        {value: 'ru_RU', label: 'на русский'},
        {value: 'ky_KG', label: 'на киргизский'},
        {value: 'uz_UZ', label: 'на узбекский'},
        {value: 'tg_TJ', label: 'на таджикский'}
      ]
      return {
        source: '123',
        result: '',
        langsFrom: langsFrom,
        langsTo: langsTo,
        langFrom: langsFrom[0].value,
        langTo: langsTo[1].value,
        loading: false
      }
    },

    methods: {
      translate () {
        if (this.source == '' || this.langFrom == this.langTo) {
          this.result = this.source;
          return;
        }
        this.loading = true;
        axios.post('/api', {
          "content": this.source,
          "lang_to": this.langTo,
          "lang_from": this.langFrom
        })
          .then((response) => {
            this.loading = false;
            this.result = response.data.content;
          })
          .catch((error) => {
            this.loading = false;
            console.log(error);
          });
      }
    },
}
</script>
