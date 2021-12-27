<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-3">
        <b-list-group>
          <b-list-group-item
              v-for="(customer, index) in customers" :key="index"
              @click="customerClicked(customer)">
            {{ customer.name }}
          </b-list-group-item>
          <b-list-group-item>
            <button
                type="button"
                class="btn btn-success btn-sm"
                v-b-modal.customer-modal>
              Add Customer
            </button>
          </b-list-group-item>
        </b-list-group>
      </div>
      <div class="col-sm-7">
        <div class="btn-group" role="group">
          <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.customer-edit-modal
                  @click="editCustomer(currentCustomer)">
              Edit
          </button>
          <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteCustomer(currentCustomer)">
              Delete
          </button>
        </div>
        <customer :customer="currentCustomer"></customer>
      </div>
    </div>
    <b-modal ref="addCustomerModal"
            id="customer-modal"
            title="Add a new Customer"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="Name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="addCustomerForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-edit-group"
                      label="Email:"
                      label-for="form-email-edit-input">
          <b-form-input id="form-email-edit-input"
                        type="text"
                        v-model="addCustomerForm.email"
                        required
                        placeholder="Enter email">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-timezone-edit-group"
                      label="Timezone:"
                      label-for="form-timezone-edit-input">
          <b-form-input id="form-timezone-edit-input"
                        type="text"
                        v-model="addCustomerForm.timezone"
                        required
                        placeholder="Enter timezone">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Add</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editCustomerModal"
            id="customer-edit-modal"
            title="Edit"
            hide-footer>
      <b-form @submit="onSubmitEdit" @reset="onResetEdit" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="Name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-edit-group"
                      label="Email:"
                      label-for="form-email-edit-input">
          <b-form-input id="form-email-edit-input"
                        type="text"
                        v-model="editForm.email"
                        required
                        placeholder="Enter email">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-timezone-edit-group"
                      label="Timezone:"
                      label-for="form-timezone-edit-input">
          <b-form-input id="form-timezone-edit-input"
                        type="text"
                        v-model="editForm.timezone"
                        required
                        placeholder="Enter timezone">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Edit</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Customer from './Customer.vue';

export default {
  name: 'Customers',
  data() {
    return {
      customers: [],
      currentCustomer: {},
      addCustomerForm: {
        name: '',
        email: '',
        timezone: '',
      },
      editForm: {
        userid: 0,
        name: '',
        email: '',
        timezone: '',
      },
    };
  },
  components: {
    Customer,
  },
  methods: {
    initForm() {
      // this.editForm.userid = 0;
      // this.editForm.name = '';
      // this.editForm.email = '';
      // this.editForm.timezone = '';
      console.log(this.currentCustomer);
      console.log(this.editForm);
    },
    getCustomers() {
      const path = 'http://localhost:5000/customers';
      axios.get(path)
        .then((res) => {
          this.customers = res.data.customers;
          this.selectFirstCustomer();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    selectFirstCustomer() {
      [this.currentCustomer] = this.customers;
    },
    customerClicked(customer) {
      this.currentCustomer = customer;
    },
    /* eslint-disable */
    editCustomer(currentCustomer) {
      this.editForm = currentCustomer;
    },
    onDeleteCustomer(currentCustomer) {
      this.removeCustomer(currentCustomer.userid);
    },
    removeCustomer(userid) {
      const path = `http://localhost:5000/customers/${userid}`;
      axios.delete(path)
        .then(() => {
          this.getCustomers();
          console.log('Customer deleted');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCustomers();
        });
    },
    onSubmitEdit(evt) {
      evt.preventDefault();
      this.$refs.editCustomerModal.hide();
      const payload = {
        name: this.editForm.name,
        email: this.editForm.email,
        timezone: this.editForm.timezone,
      };
      this.updateCustomer(payload, this.editForm.userid);
    },
    updateCustomer(payload, userid) {
      const path = `http://localhost:5000/customers/${userid}`;
      axios.put(path, payload)
        .then(() => {
          this.getCustomers();
          console.log("Customer Updated");
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCustomers();
        });
    },
    onResetEdit(evt) {
      this.$refs.editCustomerModal.hide();
      this.initForm();
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addCustomerModal.hide();
      const payload = {
        name: this.addCustomerForm.name,
        email: this.addCustomerForm.email,
        timezone: this.addCustomerForm.timezone,
      };
      this.addCustomer(payload);
      console.log('payload', payload);
      // this.initForm();
    },
    addCustomer(payload) {
      const path = 'http://localhost:5000/customers';
      axios.post(path, payload)
        .then(() => {
          this.getCustomers();
          console.log('Customer added');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getCustomers();
        });
    },
    onReset(evt) {
      evt.preventDefault();
    }
  },
  created() {
    this.getCustomers();
  },
};
</script>
