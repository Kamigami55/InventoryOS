class DeviceController < ApplicationController
  def index
  end
  def api
    #api_params = params.require(:data).permit(:username, :mode, :item_image, :item_name)
    #@username = api_params[:username]
    #@mode = api_params[:mode]
    #@item_image = api_params[:item_image]
    #@item_name = api_params[:item_name]
    @username = params[:username]
    @mode = params[:mode]
    @item_name = params[:item_name]

    # Main logic here

    # find user
    @user = User.find_by_name(@username)
    if @user.nil?
      # show error page: user not found TODO
      render inline: "User <%= @username %> not found"
      return
    end

    if @mode == 'BORROW'
      @item = Item.where(name: @item_name, holder_id: nil).first

      if not @item.nil?
        # item in inventory and availiable
        # set item holder to user
        #@item = @item.first
        @item.holder = @user
        @item.save
        # show msg TODO
        render inline: "Item <%= @item.name %> borrowed by <%= @item.holder.name %>"
        return
      else
        #     //add item to inventory
        #     //set item holder to user
        #     //show edit page(can easily delete)
        # show error msg TODO
        render inline: "Item <%= @item_name %> not found"
        return
      end
      # End BORROW

    elsif @mode == 'RETURN'
      @item = @user.held_items.find_by_name(@item_name)
      if not @item.nil?
        # the item the user is holding
        # set no holder for this item
        @item.holder = nil
        @item.save
        # show msg TODO
        render inline: "Item <%= @item.name %> returned by <%= @user.name %>"
        return
      else
        # show error msg
        render inline: "User <%= @user.name %> not holding this item <%= @item_name %>"
        return
      end
      # End RETURN

    elsif @mode == 'ADDNEW'
      # add item to inventory
      @item = Item.new(name: @item_name)
      # set owner to user
      @item.owner = @user
      @item.save
      # show edit page TODO
      render inline: "Item <%= @item.name %> owned by <%= @item.owner.name %> added"
      return
      # End ADDNEW
    end

    render inline: "ERROR: <%= @username || 'null' %> <%= @mode || 'null' %> <%= @item_image || 'null' %> <%= @item_name || 'null' %>"
    return
  end
  # End api
end
# End class
