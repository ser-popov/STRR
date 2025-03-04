<script setup lang="ts">
import type { Form } from '#ui/types'
const { t } = useI18n()
const { getBusinessSchema } = useStrrPlatformBusiness()
const { platformBusiness, isMailingInBC } = storeToRefs(useStrrPlatformBusiness())

const props = defineProps<{ isComplete: boolean }>()

// cant set form schema type as businessDetailsSchema is a computed property
const platformBusinessFormRef = ref<Form<any>>()

const getRadioOptions = () => [
  { value: true, label: t('word.Yes') },
  { value: false, label: t('word.No') }
]

// reset cpbcLicenceNumber if hasCpbc radio button changed
watch(() => platformBusiness.value.hasCpbc, () => {
  platformBusiness.value.cpbcLicenceNumber = ''
})

// set regOfficeOrAtt.mailingAddress to match business mailing address if sameAsMailAddress checkbox checked
watch(() => platformBusiness.value.regOfficeOrAtt.sameAsMailAddress,
  (newVal) => {
    if (newVal) {
      // revalidate fields to update/remove form errors
      platformBusinessFormRef.value?.validate([
        'regOfficeOrAtt.mailingAddress.country',
        'regOfficeOrAtt.mailingAddress.street',
        'regOfficeOrAtt.mailingAddress.city',
        'regOfficeOrAtt.mailingAddress.region',
        'regOfficeOrAtt.mailingAddress.postalCode'
      ], { silent: true })
    }
  }
)

watch(() => platformBusiness.value.hasRegOffAtt,
  (_, oldVal) => {
    // revalidate fields to update/remove form errors if user clicks yes or no
    // only revalidate if not the first click
    if (oldVal !== undefined) {
      platformBusinessFormRef.value?.validate([
        'hasRegOffAtt',
        'regOfficeOrAtt.mailingAddress.country',
        'regOfficeOrAtt.mailingAddress.street',
        'regOfficeOrAtt.mailingAddress.city',
        'regOfficeOrAtt.mailingAddress.region',
        'regOfficeOrAtt.mailingAddress.postalCode'
      ], { silent: true })
    }
  }
)

onMounted(async () => {
  // validate form if step marked as complete
  if (props.isComplete) {
    await validateForm(platformBusinessFormRef.value, props.isComplete)
  }
})
</script>

<template>
  <div data-testid="business-details">
    <ConnectPageSection
      class="bg-white"
      :heading="{ label: $t('strr.section.title.businessInfo'), labelClass: 'font-bold md:ml-6' }"
    >
      <UForm
        ref="platformBusinessFormRef"
        :schema="getBusinessSchema()"
        :state="platformBusiness"
        class="space-y-10 py-10"
      >
        <ConnectFormSection
          :title="$t('strr.section.subTitle.businessIds')"
          :error="isComplete && (platformBusiness.hasCpbc === undefined ||
            hasFormErrors(platformBusinessFormRef, ['legalName', 'homeJurisdiction', 'cpbcLicenceNumber']))
          "
        >
          <div class="space-y-5">
            <ConnectFormFieldGroup
              id="platform-business-legal-name"
              v-model="platformBusiness.legalName"
              :aria-label="$t('label.legalName')"
              :help="$t('strr.hint.businessLegalNamePlatform')"
              name="legalName"
              :placeholder="$t('label.legalName')"
              :is-required="true"
            />
            <ConnectFormFieldGroup
              id="platform-business-home-jur"
              v-model="platformBusiness.homeJurisdiction"
              :aria-label="$t('label.homeJurisdictionOpt')"
              :help="$t('strr.hint.humeJurisdiction')"
              name="homeJurisdiction"
              :placeholder="t('label.homeJurisdictionOpt')"
              :is-required="true"
            />
            <ConnectFormFieldGroup
              id="platform-business-number"
              v-model="platformBusiness.businessNumber"
              :aria-label="$t('label.busNumOpt')"
              name="businessNumber"
              :placeholder="$t('label.busNumOpt')"
              :help="$t('strr.hint.businessNumber')"
              mask="#########@@####"
            />
            <UFormGroup
              id="platform-business-hasCpbc"
              data-testid="platform-business-hasCpbc"
              name="hasCpbc"
            >
              <URadioGroup
                v-model="platformBusiness.hasCpbc"
                class="p-2"
                :class="isComplete && platformBusiness.hasCpbc === undefined ? 'border-red-600 border-2' : ''"
                :options="getRadioOptions()"
                :ui="{ legend: 'mb-3 text-default font-bold text-gray-700' }"
                :ui-radio="{ inner: 'space-y-2' }"
              >
                <template #legend>
                  <span class="sr-only">{{ $t('validation.required') }}</span>
                  <span>{{ $t('strr.text.hasCpbc') }}</span>
                </template>
              </URadioGroup>
            </UFormGroup>
            <ConnectFormFieldGroup
              v-if="platformBusiness.hasCpbc"
              id="platform-cpbc"
              v-model="platformBusiness.cpbcLicenceNumber"
              :aria-label="$t('label.cpbcLicNum')"
              name="cpbcLicenceNumber"
              :placeholder="$t('label.cpbcLicNum')"
              :is-required="true"
            />
          </div>
        </ConnectFormSection>
        <div class="h-px w-full border-b border-gray-100" />
        <ConnectFormSection
          :title="$t('strr.section.subTitle.businessMailAddress')"
          :error="hasFormErrors(platformBusinessFormRef, [
            'mailingAddress.country',
            'mailingAddress.street',
            'mailingAddress.city',
            'mailingAddress.region',
            'mailingAddress.postalCode'
          ])"
        >
          <div class="max-w-bcGovInput">
            <ConnectFormAddress
              id="platform-business-address"
              v-model:country="platformBusiness.mailingAddress.country"
              v-model:street="platformBusiness.mailingAddress.street"
              v-model:street-additional="platformBusiness.mailingAddress.streetAdditional"
              v-model:city="platformBusiness.mailingAddress.city"
              v-model:region="platformBusiness.mailingAddress.region"
              v-model:postal-code="platformBusiness.mailingAddress.postalCode"
              :schema-prefix="'mailingAddress.'"
              :form-ref="platformBusinessFormRef"
              :excluded-fields="['streetName', 'streetNumber', 'unitNumber']"
            />
          </div>
        </ConnectFormSection>
        <div class="h-px w-full border-b border-gray-100" />
        <ConnectFormSection
          :title="$t('strr.section.subTitle.regOfficeAttSvcAddrress')"
          :error="hasFormErrors(platformBusinessFormRef, [
            'hasRegOffAtt',
            'regOfficeOrAtt.mailingAddress.country',
            'regOfficeOrAtt.mailingAddress.street',
            'regOfficeOrAtt.mailingAddress.city',
            'regOfficeOrAtt.mailingAddress.region',
            'regOfficeOrAtt.mailingAddress.postalCode'
          ])"
        >
          <div class="max-w-bcGovInput space-y-5">
            <UFormGroup
              id="platform-business-hasRegOffAtt"
              data-testid="platform-business-hasRegOffAtt"
              name="hasRegOffAtt"
            >
              <URadioGroup
                v-model="platformBusiness.hasRegOffAtt"
                class="p-2"
                :class="isComplete && platformBusiness.hasRegOffAtt === undefined ? 'border-red-600 border-2' : ''"
                :options="getRadioOptions()"
                :ui="{ legend: 'mb-3 text-default font-bold text-gray-700' }"
                :ui-radio="{ inner: 'space-y-2' }"
              >
                <template #legend>
                  <span class="sr-only">{{ $t('validation.required') }}</span>
                  <span>{{ $t('strr.text.regOffOrAtt') }}</span>
                </template>
              </URadioGroup>
            </UFormGroup>
            <div v-if="platformBusiness.hasRegOffAtt" class="space-y-5">
              <UFormGroup name="null">
                <UCheckbox
                  v-if="isMailingInBC"
                  v-model="platformBusiness.regOfficeOrAtt.sameAsMailAddress"
                  :label="t('label.sameAsMailAddress')"
                />
              </UFormGroup>
              <ConnectFormFieldGroup
                id="platform-att-for-svc-name"
                v-model="platformBusiness.regOfficeOrAtt.attorneyName"
                :aria-label="$t('strr.label.attForSvcName')"
                name="regOfficeOrAtt.attorneyName"
                :placeholder="$t('strr.label.attForSvcName')"
              />
              <ConnectFormAddress
                v-if="!platformBusiness.regOfficeOrAtt.sameAsMailAddress"
                id="platform-registered-office-address"
                v-model:country="platformBusiness.regOfficeOrAtt.mailingAddress.country"
                v-model:street="platformBusiness.regOfficeOrAtt.mailingAddress.street"
                v-model:street-additional="platformBusiness.regOfficeOrAtt.mailingAddress.streetAdditional"
                v-model:city="platformBusiness.regOfficeOrAtt.mailingAddress.city"
                v-model:region="platformBusiness.regOfficeOrAtt.mailingAddress.region"
                v-model:postal-code="platformBusiness.regOfficeOrAtt.mailingAddress.postalCode"
                :schema-prefix="'regOfficeOrAtt.mailingAddress.'"
                :disabled-fields="['country', 'region']"
                :excluded-fields="['streetName', 'streetNumber', 'unitNumber']"
                :form-ref="platformBusinessFormRef"
              />
            </div>
          </div>
        </ConnectFormSection>
        <div class="h-px w-full border-b border-gray-100" />
        <ConnectFormSection
          :title="$t('strr.section.subTitle.noticeNonCompliance')"
          :error="hasFormErrors(platformBusinessFormRef, ['nonComplianceEmail'])"
        >
          <div class="space-y-5">
            <i18n-t tag="p" keypath="strr.text.nonComplianceEmail" scope="global">
              <template #learnMore>
                <UButton
                  :to="useRuntimeConfig().public.platformsLearnMoreUrl"
                  :external="true"
                  target="_blank"
                  variant="link"
                  :padded="false"
                  trailing-icon="i-mdi-open-in-new"
                  :label="$t('btn.learnMore')"
                  :ui="{
                    icon: {
                      size: {
                        sm: 'h-4 w-4'
                      }
                    },
                    gap: { sm: 'gap-x-1.5' }
                  }"
                />
              </template>
            </i18n-t>
            <ConnectFormFieldGroup
              id="platform-business-noncompliance-email"
              v-model="platformBusiness.nonComplianceEmail"
              :aria-label="$t('label.emailAddress')"
              name="nonComplianceEmail"
              :placeholder="$t('label.emailAddress')"
              :is-required="true"
              type="email"
            />
            <ConnectFormFieldGroup
              id="platform-business-noncompliance-email-optional"
              v-model="platformBusiness.nonComplianceEmailOptional"
              :aria-label="$t('label.emailAddressOpt')"
              name="nonComplianceEmailOptional"
              :placeholder="$t('label.emailAddressOpt')"
              type="email"
            />
          </div>
        </ConnectFormSection>
        <div class="h-px w-full border-b border-gray-100" />
        <ConnectFormSection
          :title="$t('strr.section.subTitle.takedownRequest')"
          :error="hasFormErrors(platformBusinessFormRef, ['takeDownEmail'])"
        >
          <div class="space-y-5">
            <i18n-t tag="p" keypath="strr.text.takedownEmail" scope="global">
              <template #learnMore>
                <UButton
                  :to="useRuntimeConfig().public.platformsLearnMoreUrl"
                  target="_blank"
                  :external="true"
                  variant="link"
                  :padded="false"
                  trailing-icon="i-mdi-open-in-new"
                  :label="$t('btn.learnMore')"
                  :ui="{
                    icon: {
                      size: {
                        sm: 'h-4 w-4'
                      }
                    },
                    gap: { sm: 'gap-x-1.5' }
                  }"
                />
              </template>
            </i18n-t>
            <ConnectFormFieldGroup
              id="platform-business-takedown-email"
              v-model="platformBusiness.takeDownEmail"
              :aria-label="$t('label.emailAddress')"
              name="takeDownEmail"
              :placeholder="$t('label.emailAddress')"
              :is-required="true"
              type="email"
            />
            <ConnectFormFieldGroup
              id="platform-business-takedown-email-optional"
              v-model="platformBusiness.takeDownEmailOptional"
              :aria-label="$t('label.emailAddressOpt')"
              name="takeDownEmailOptional"
              :placeholder="$t('label.emailAddressOpt')"
              type="email"
            />
          </div>
        </ConnectFormSection>
      </UForm>
    </ConnectPageSection>
  </div>
</template>
