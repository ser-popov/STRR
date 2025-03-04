<script setup lang="ts">
import type { Form } from '#ui/types'
import { z } from 'zod'

const props = defineProps<{
  setOwner?: HostOwner,
  ownerType: OwnerType,
  isComplete: boolean,
  hideHeading?: boolean
}>()

provide<OwnerRole | undefined>('originalRole', props.setOwner?.role)

const emit = defineEmits<{
  cancel: [],
  done: [HostOwner]
}>()

const { getHostOwnerSchema, getNewHostOwner } = useHostOwnerStore()
const { activeOwner } = storeToRefs(useHostOwnerStore())

// Only init 'showErrors' with 'isComplete' value if this owner was already initialized previously
const showErrors = ref(activeOwner.value ? props.isComplete : false)

const owner = ref<HostOwner>(props.setOwner
  ? JSON.parse(JSON.stringify(props.setOwner))
  : getNewHostOwner(false, props.ownerType))

const ownerSchema = computed(() => getHostOwnerSchema(owner.value.ownerType, owner.value.role))
const ownerFormRef = ref<Form<z.output<typeof ownerSchema.value>>>()

watch(owner, (val) => { activeOwner.value = val }, { immediate: true })
watch(() => owner.value.role, async (newVal, oldVal) => {
  // clear fields that change meaning depending on if the entity is a host
  if ([newVal, oldVal].includes(OwnerRole.HOST)) {
    owner.value.taxNumber = ''
    owner.value.dateOfBirth = ''
    owner.value.mailingAddress = {
      street: '',
      streetAdditional: '',
      region: '',
      city: '',
      country: '',
      postalCode: '',
      locationDescription: ''
    }
    // Needs to trigger validate so that form registers the 'clear'
    await ownerFormRef.value?.validate(['mailingAddress.postalCode', 'taxNumber'], { silent: true })
    ownerFormRef.value?.clear('mailingAddress.postalCode')
    ownerFormRef.value?.clear('taxNumber')
  }
})

const saveOwner = async () => {
  const errors = await validateForm(ownerFormRef.value, true)
  if (!errors) {
    emit('done', owner.value)
  } else {
    showErrors.value = true
    // TODO: scroll to error?
    console.info(errors)
  }
}

onMounted(async () => {
  await validateForm(ownerFormRef.value, showErrors.value)
})
</script>

<template>
  <div data-testid="host-owner">
    <UForm
      ref="ownerFormRef"
      :schema="ownerSchema"
      :state="owner"
      class="space-y-10"
    >
      <ConnectPageSection
        v-if="ownerFormRef"
        class="bg-white"
        :heading="hideHeading ? undefined : {
          bgColor: 'white',
          label: owner.ownerType === OwnerType.INDIVIDUAL
            ? $t('strr.section.title.addIndividual')
            : $t('strr.section.title.addBusiness'),
          labelClass: 'font-bold md:ml-6'
        }"
      >
        <div class="py-10">
          <div v-if="owner.ownerType === OwnerType.INDIVIDUAL">
            <FormAddOwnersInputPerson
              v-model:owner="owner"
              v-model:owner-form-ref="ownerFormRef"
              :show-errors="showErrors"
              show-roles
              show-btns
              @cancel="$emit('cancel')"
              @done="saveOwner()"
            />
          </div>
          <div v-else>
            <FormAddOwnersInputBusiness
              v-model:owner="owner"
              v-model:owner-form-ref="ownerFormRef"
              :show-btns="!owner.role"
              :show-errors="showErrors"
              show-roles
              @cancel="$emit('cancel')"
              @done="saveOwner()"
            />
            <ConnectPageSection
              v-if="!!owner.role"
              class="mt-10 rounded-none border-t border-gray-200 bg-white shadow-none ring-0"
              :heading="{
                bgColor: 'white',
                icon: 'i-mdi-account-circle',
                iconClass: 'text-gray-700 size-5 md:ml-6',
                label: $t('strr.section.title.contactIndividualDetails'),
                labelClass: 'font-bold'
              }"
            >
              <div class="mt-10 space-y-10">
                <p class="ml-10">
                  {{ $t('strr.text.businessContactIndividual') }}
                </p>
                <FormAddOwnersInputPerson
                  v-model:owner="owner"
                  v-model:owner-form-ref="ownerFormRef"
                  :show-errors="showErrors"
                  show-btns
                  @cancel="$emit('cancel')"
                  @done="saveOwner()"
                />
              </div>
            </ConnectPageSection>
          </div>
        </div>
      </ConnectPageSection>
    </UForm>
  </div>
</template>
