(function () {
    function populate(select, items, placeholder) {
        select.innerHTML = "";
        var empty = document.createElement("option");
        empty.value = "";
        empty.textContent = placeholder;
        select.appendChild(empty);
        items.forEach(function (item) {
            var option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.name;
            select.appendChild(option);
        });
    }

    function fetchJSON(url) {
        return fetch(url).then(function (response) {
            return response.json();
        }).then(function (data) {
            return data.results !== undefined ? data.results : data;
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        var typeSelect = document.getElementById("id_type");
        var categorySelect = document.getElementById("id_category");
        var subcategorySelect = document.getElementById("id_subcategory");

        if (!typeSelect || !categorySelect || !subcategorySelect) {
            return;
        }

        typeSelect.addEventListener("change", function () {
            if (!typeSelect.value) {
                populate(categorySelect, [], "Сначала выберите тип");
                populate(subcategorySelect, [], "Сначала выберите категорию");
                return;
            }
            fetchJSON("/api/categories/?type=" + typeSelect.value).then(function (categories) {
                populate(categorySelect, categories, "Выберите категорию");
                populate(subcategorySelect, [], "Сначала выберите категорию");
            });
        });

        categorySelect.addEventListener("change", function () {
            if (!categorySelect.value) {
                populate(subcategorySelect, [], "Сначала выберите категорию");
                return;
            }
            fetchJSON("/api/subcategories/?category=" + categorySelect.value).then(function (subcategories) {
                populate(subcategorySelect, subcategories, "Выберите подкатегорию");
            });
        });
    });
})();
