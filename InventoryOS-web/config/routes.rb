Rails.application.routes.draw do
  root :to => 'main#index'
  resources :items
  resources :users
end
