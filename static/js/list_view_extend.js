/**
 * Created by admin on 2017/3/7.
 */
var ListView = require('web.ListView');

var ListViewExtend = ListView.extend({
    load_list: function() {
        debugger
        var self = this;
        // console.log('load list',this);
        // alert('load list');
        // Render the table and append its content
        if (this.model == "goose.order"){
            this.$el.html(QWeb.render("ListView2",this))
        }
        else{
            this.$el.html(QWeb.render(this._template, this));
        }
        this.$el.addClass(this.fields_view.arch.attrs['class']);
        if (this.grouped) {
            this.$('.o_list_view').addClass('o_list_view_grouped');
        }
        this.$('.o_list_view').append(this.groups.elements);

        // Compute the aggregates and display them in the list's footer
        this.compute_aggregates();

        // Head hook
        // Selecting records
        this.$('thead .o_list_record_selector input').click(function() {
            self.$('tbody .o_list_record_selector input').prop('checked', $(this).prop('checked') || false);
            var selection = self.groups.get_selection();
            $(self.groups).trigger('selected', [selection.ids, selection.records]);
        });

        // Sort
        if (this.dataset._sort.length) {
            if (this.dataset._sort[0].indexOf('-') === -1) {
                this.$('th[data-id=' + this.dataset._sort[0] + ']').addClass("o-sort-down");
            } else {
                this.$('th[data-id=' + this.dataset._sort[0].split('-')[1] + ']').addClass("o-sort-up");
            }
        }

        this.trigger('list_view_loaded', data, this.grouped);
        return $.when();
    },
})