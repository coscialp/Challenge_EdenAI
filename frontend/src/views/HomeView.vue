<template>
  <NavBar />
  <main>
    <section class="card upload-files">
      <input
        id="file"
        class="input-file"
        type="file"
        multiple
        accept="image/jpeg,image/png,.pdf"
        @change="handleFilesUpload($event)"
      />
      <button
        class="button"
        :class="{ 'button--disable': filesIsEmpty }"
        @click="submitFiles()"
      >
        Submit
        <font-awesome-icon icon="fa-solid fa-upload" />
      </button>
    </section>
    <section class="card list-files">
      <h1 class="list-files__title">Your files</h1>
      <v-table class="list-files__table" :data="files">
        <thead>
          <th>Name</th>
          <th>Type</th>
          <th>Size</th>
          <th class="clickable" @click="sortByAdded()">
            Added
            <font-awesome-icon
              icon="fa-solid fa-caret-up"
              v-if="reversed === true"
            />
            <font-awesome-icon icon="fa-solid fa-caret-down" v-else />
          </th>
        </thead>
        <tbody>
          <tr v-for="file in displayFiles" :key="file.id">
            <td>
              <a :href="`http://localhost:8000/media/${file.name}`">{{
                file.name
              }}</a>
            </td>
            <td>
              <font-awesome-icon
                class="icon"
                :icon="getIconFileType(file.filetype)"
              />
            </td>
            <td>{{ getSize(file.size) }}</td>
            <td>{{ formatDate(file.since_added) }}</td>
          </tr>
        </tbody>
      </v-table>
    </section>
  </main>
</template>

<script>
import NavBar from "@/components/Navbar";
import { mapState } from "vuex";
import moment from "moment";

export default {
  name: "HomeView",
  components: {
    NavBar,
  },
  data: function () {
    return {
      filesToUpload: null,
      reversed: false,
    };
  },
  mounted() {
    this.$store.commit("setCurrentFiles");
    console.log("Je suis monté sur le DOM!");
  },
  computed: {
    filesIsEmpty: function () {
      return this.filesToUpload === null || !this.filesToUpload[0];
    },
    ...mapState(["files", "displayFiles", "status"]),
  },
  methods: {
    handleFilesUpload: function (event) {
      this.filesToUpload = event.target.files;
    },
    submitFiles: function () {
      let formData = new FormData();
      for (let i = 0; i < this.filesToUpload.length; i++) {
        formData.append(`file`, this.filesToUpload[i]);
        formData.append(`owner`, this.$store.state.user.id);
        this.$store.dispatch("submitFile", formData);
      }
      this.$store.commit("setStatus", "create");
    },
    getSize: function (size) {
      let size_inKB = (size / 1000).toPrecision(3);
      if (size_inKB > 100000) {
        return size_inKB / 1000000 + "GB";
      } else if (size_inKB > 1000) {
        return size_inKB / 1000 + "MB";
      } else {
        return size_inKB + "KB";
      }
    },
    getIconFileType: function (type) {
      let icon = "";
      if (type === "pdf") {
        icon = "fa-file-pdf";
      } else if (type === "jpeg" || type === "png") {
        icon = "fa-file-image";
      } else {
        icon = "fa-file";
      }
      return "fa-solid " + icon;
    },
    formatDate: function (value) {
      if (value) {
        return moment(String(value)).format("MM/DD/YYYY");
      }
    },
    sortByAdded: function () {
      if (this.reversed === true) {
        this.$store.commit("reverseSortByAdded");
        this.reversed = false;
      } else {
        this.$store.commit("sortByAdded");
        this.reversed = true;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../styles/variables";

main {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 32px;
  gap: 32px;
  flex-direction: column;
}

.card {
  width: 1080px;
  padding: 32px;
  background-color: white;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.upload-files {
  min-height: 15vh;
}

.list-files {
  max-height: 50vh;

  &__title {
    text-align: center;
    color: $primary-color;
    font-size: 20px;
    font-weight: 700;
    text-underline: $primary-color;
  }

  &__table {
    padding: 16px;
    table-layout: fixed;
    overflow-y: scroll;
    a {
      color: black;
      text-decoration: none;
    }

    th {
      padding-top: 12px;
      padding-bottom: 12px;
      text-align: left;
      background-color: $primary-color;
      color: white;
    }

    .clickable {
      cursor: pointer;
    }

    td,
    th {
      min-width: 200px;
      text-align: center;
      vertical-align: middle;
      border: 1px solid #ddd;
      padding: 8px;
    }

    tr {
      &:nth-child(even) {
        background-color: #f2f2f2;
      }

      &:hover {
        background-color: #ddd;
      }
    }
  }
}

.icon {
  color: $primary-color;
}

.button {
  width: 100px;
}

.input-file {
  border: 5px double $button-background-color--disable;
  border-radius: 50px;
  background-color: #f2f2f2;
  width: 100%;
  padding: 2px;
  font-size: 14px;

  &::-webkit-file-upload-button {
    background: $primary-color;
    color: white;
    font-weight: 700;
    border: none;
    padding: 8px 16px;
    border-radius: 50px;
    cursor: pointer;

    &:hover {
      background: $secondary-color;
    }
  }
}
</style>
